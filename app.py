from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify, flash
import psycopg2
from functools import wraps
import csv
import io
from datetime import datetime, timedelta
import os

# ==================== CONFIGURATION FLASK ====================
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'edt-faculte-secret-key-2025')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True


# ==================== CONTEXT PROCESSOR ====================
@app.context_processor
def inject_datetime():
    return dict(
        datetime=datetime,
        now=datetime.now,
        timedelta=timedelta,
        len=len,
        str=str,
        int=int,
        list=list,
        dict=dict
    )


# ==================== BASE DE DONNÉES (OPTIONNEL) ====================
db_config = {
    'host': 'dpg-d5n77g6mcj7s73cgqnt0-a.frankfurt-postgres.render.com',
    'user': 'mydb_v0t8_users',
    'password': '3nZmE3DRpoD6E7SeF7zk5oHjhoMAKlhh',
    'database': 'mydb_v0t8',
    'port': 5432
}


# ==================== DÉCORATEURS ====================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'app_user' not in session:
            flash("Veuillez vous connecter", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'app_user' not in session:
                return redirect(url_for('login'))
            if session.get('role') != role:
                flash("Accès non autorisé", "danger")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ==================== PLANNING SIMULÉ ====================
def generer_planning_simule(date_debut, departement, nb_jours=7):
    date_obj = datetime.strptime(date_debut, "%Y-%m-%d")
    heures = ['08:00', '10:00', '14:00', '16:00']
    salles = ['Salle 101', 'Salle 102', 'Amphi A', 'Amphi B']

    planning = []
    for i in range(nb_jours):
        planning.append({
            'id_examen': 1000 + i,
            'departement': departement,
            'nom_module': f"Module {i+1}",
            'date_exam': (date_obj + timedelta(days=i)).strftime("%Y-%m-%d"),
            'heure_debut': heures[i % len(heures)],
            'nom_salle': salles[i % len(salles)],
            'professeur': f"Prof. Enseignant{i+1}",
            'capacite_salle': 50,
            'nb_etudiants': 30 + i,
            'statut': "OK"
        })
    return planning


# ==================== CONFLITS ====================
def detecter_conflits(planning):
    conflits = []
    used = set()

    for e in planning:
        key = f"{e['date_exam']}_{e['heure_debut']}_{e['nom_salle']}"
        if key in used:
            conflits.append({
                'type': 'SALLE',
                'message': f"Conflit salle {e['nom_salle']} le {e['date_exam']} à {e['heure_debut']}"
            })
        else:
            used.add(key)
    return conflits


# ==================== EXPORT CSV ====================
def exporter_csv(data):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    if data:
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())
    output.seek(0)
    return output.getvalue()


# ==================== LOGIN ====================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = psycopg2.connect(
                host='dpg-d5n77g6mcj7s73cgqnt0-a.frankfurt-postgres.render.com',
                user='mydb_v0t8_users',
                password='3nZmE3DRpoD6E7SeF7zk5oHjhoMAKlhh',
                dbname='mydb_v0t8',
                port=5432
            )
            cur = conn.cursor()

            cur.execute("""
                SELECT username, role, departement
                FROM app_user
                WHERE username = %s AND password = %s
            """, (username, password))

            user = cur.fetchone()

            cur.close()
            conn.close()

            if user:
                session['app_user'] = user[0]
                session['role'] = user[1]
                session['departement'] = user[2]

                flash("Connexion réussie", "success")

                routes = {
                    'etudiant': 'etudiant_dashboard',
                    'professeur': 'professeur_dashboard',
                    'administrateur': 'administrateur_dashboard'
                }
                return redirect(url_for(routes[user[1]]))
            else:
                flash("Identifiants incorrects", "danger")

        except Exception as e:
            flash("Erreur de connexion à la base de données", "danger")
            print(e)

    return render_template("interface.html")




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ==================== ÉTUDIANT ====================
@app.route('/etudiant/dashboard')
@role_required('etudiant')
def etudiant_dashboard():
    return render_template("etudiant.html")


@app.route('/etudiant/planning', methods=['GET', 'POST'])
@role_required('etudiant')
def planning_etudiant():
    planning = []
    conflits = []

    if request.method == 'POST':
        date_debut = request.form['date_debut']
        planning = generer_planning_simule(date_debut, session['departement'])
        conflits = detecter_conflits(planning)

    return render_template("planning_etudiant.html", planning=planning, conflits=conflits)


@app.route('/etudiant/export_csv')
@role_required('etudiant')
def export_csv_etudiant():
    planning = generer_planning_simule(datetime.now().strftime('%Y-%m-%d'), session['departement'])
    csv_content = exporter_csv(planning)

    response = make_response(csv_content)
    response.headers["Content-Disposition"] = "attachment; filename=planning.csv"
    response.headers["Content-type"] = "text/csv"
    return response


# ==================== PROFESSEUR ====================
@app.route('/professeur/dashboard')
@role_required('professeur')
def professeur_dashboard():
    return render_template("professeur.html")


# ==================== ADMINISTRATEUR ====================
@app.route('/administrateur/dashboard')
@role_required('administrateur')
def administrateur_dashboard():
    return render_template("administrateur.html")


@app.route('/administrateur/generer', methods=['GET', 'POST'])
@role_required('administrateur')
def generer_edt():
    planning = []
    conflits = []

    if request.method == 'POST':
        date_debut = request.form['date_debut']
        departement = request.form['departement']
        planning = generer_planning_simule(date_debut, departement)
        conflits = detecter_conflits(planning)

    return render_template("generer_edt.html", planning=planning, conflits=conflits)


@app.route('/administrateur/conflits', methods=['GET', 'POST'])
@role_required('administrateur')
def conflits_admin():
    conflits = []

    if request.method == 'POST':
        date_debut = request.form['date_debut']
        departement = request.form['departement']
        planning = generer_planning_simule(date_debut, departement)
        conflits = detecter_conflits(planning)

    return render_template("detecter_conflits.html", conflits=conflits)


# ==================== MAIN ====================


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fournit le PORT via variable d'environnement
    app.run(host="0.0.0.0", port=port, debug=True)

