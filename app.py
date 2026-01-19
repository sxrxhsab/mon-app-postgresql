from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify, flash
import psycopg2
from functools import wraps
import csv
import io
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
import traceback

# ==================== CONFIGURATION FLASK ====================
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'edt-faculte-secret-key-2025')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
# À mettre sur True en production avec HTTPS
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# ==================== CONTEXT PROCESSOR ====================


@app.context_processor
def inject_datetime():
    """Injection de variables dans tous les templates"""
    return {
        'datetime': datetime,
        'now': datetime.now,
        'timedelta': timedelta,
        'len': len,
        'str': str,
        'int': int,
        'list': list,
        'dict': dict
    }


# ==================== CONFIGURATION BASE DE DONNÉES ====================
db_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'VOTRE_MDP_POSTGRES',
    'database': 'NOM_BASE_POSTGRES',
    'port': 5432,

}

# ==================== CONFIGURATION EMAIL ====================
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'votre.email@gmail.com',
    'password': 'votre_mot_de_passe',
    'from_email': 'noreply@edt-faculte.com'
}

# ==================== DÉCORATEURS ====================


def login_required(f):
    """Décorateur pour exiger une connexion"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Veuillez vous connecter pour accéder à cette page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """Décorateur pour exiger un rôle spécifique"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                flash('Veuillez vous connecter', 'warning')
                return redirect(url_for('login'))
            if session.get('role') != required_role:
                flash('Accès non autorisé pour votre rôle', 'danger')
                # Redirection selon le rôle
                role_routes = {
                    'etudiant': 'etudiant_dashboard',
                    'professeur': 'professeur_dashboard',
                    'administrateur': 'administrateur_dashboard',
                    'chef_departement': 'chef_departement_dashboard',
                    'doyen': 'doyen_dashboard'
                }
                return redirect(
    url_for(
        role_routes.get(
            session.get('role'),
             'login')))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_db_connection():
    """Établit une connexion à la base de données avec gestion d'erreur"""
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.Error as err:
        print(f"⚠️ Erreur de connexion DB: {err}")
        return None

# ==================== FONCTIONS UTILITAIRES ====================


def generer_planning_simule(
    date_debut=None,
    departement='Informatique',
     nb_jours=7):
    """Génère un planning simulé pour les tests"""
    try:
        if date_debut:
            if isinstance(date_debut, str):
                date_obj = datetime.strptime(date_debut, '%Y-%m-%d')
            else:
                date_obj = date_debut
        else:
            date_obj = datetime.now()
    except (ValueError, TypeError):
        date_obj = datetime.now()

    planning = []

    # Départements et formations
    formations_par_departement = {
        'Informatique': ['Licence Informatique', 'Master Informatique', 'Licence MIAGE'],
        'Mathématiques': ['Licence Mathématiques', 'Master Mathématiques', 'Licence Math-Info'],
        'Physique': ['Licence Physique', 'Master Physique', 'Licence Physique-Chimie'],
        'Chimie': ['Licence Chimie', 'Master Chimie', 'Licence Chimie-Biologie'],
        'Biologie': ['Licence Biologie', 'Master Biologie', 'Licence Biochimie']
    }

    # Modules par département
    modules_par_departement = {
        'Informatique': [
            'Algorithmique Avancée', 'Base de Données', 'Réseaux Informatiques',
            'Programmation Web', 'Intelligence Artificielle', 'Sécurité Informatique',
            'Systèmes d\'Exploitation', 'Développement Mobile'
        ],
        'Mathématiques': [
            'Algèbre Linéaire', 'Analyse Mathématique', 'Statistiques',
            'Probabilités', 'Calcul Différentiel', 'Topologie',
            'Théorie des Nombres', 'Équations Différentielles'
        ],
        'Physique': [
            'Mécanique Quantique', 'Électromagnétisme', 'Thermodynamique',
            'Mécanique Classique', 'Optique', 'Physique Nucléaire',
            'Astrophysique', 'Physique des Matériaux'
        ],
        'Chimie': [
            'Chimie Organique', 'Biochimie', 'Chimie Analytique',
            'Chimie Inorganique', 'Chimie Physique', 'Chimie des Polymères',
            'Spectroscopie', 'Chimie Théorique'
        ],
        'Biologie': [
            'Génétique', 'Biologie Moléculaire', 'Microbiologie',
            'Biologie Cellulaire', 'Écologie', 'Physiologie Animale',
            'Biologie Végétale', 'Immunologie'
        ]
    }

    # Salles par type
    salles = {
        'Amphi': ['Amphi A', 'Amphi B', 'Amphi C', 'Amphi D'],
        'Salle': ['Salle 101', 'Salle 102', 'Salle 103', 'Salle 104', 'Salle 105',
                  'Salle 201', 'Salle 202', 'Salle 203', 'Salle 204', 'Salle 205'],
        'Laboratoire': ['Lab Info A', 'Lab Info B', 'Lab Physique', 'Lab Chimie', 'Lab Biologie']
    }

    # Professeurs
    professeurs = [
        {'nom': 'Belkacmi', 'prenom': 'Ahmed', 'specialite': 'Informatique'},
        {'nom': 'Amir', 'prenom': 'Karim', 'specialite': 'Mathématiques'},
        {'nom': 'Djedai', 'prenom': 'Sofia', 'specialite': 'Physique'},
        {'nom': 'Smith', 'prenom': 'John', 'specialite': 'Chimie'},
        {'nom': 'Johnson', 'prenom': 'Emma', 'specialite': 'Biologie'},
        {'nom': 'Martin', 'prenom': 'Pierre', 'specialite': 'Informatique'},
        {'nom': 'Dubois', 'prenom': 'Marie', 'specialite': 'Mathématiques'},
        {'nom': 'Robert', 'prenom': 'Luc', 'specialite': 'Physique'}
    ]

    # Heures possibles
    heures = [
    '08:00',
    '09:00',
    '10:00',
    '11:00',
    '14:00',
    '15:00',
    '16:00',
     '17:00']

    # Génération des examens
    for i in range(min(nb_jours, 10)):  # Maximum 10 examens
        date_exam = date_obj + timedelta(days=i)

        # Formation aléatoire pour le département
        formations = formations_par_departement.get(
            departement, ['Licence Générale'])
        formation = formations[i % len(formations)]

        # Module aléatoire pour le département
        modules = modules_par_departement.get(departement, ['Module Général'])
        module = modules[i % len(modules)]

        # Type de salle selon le type d'examen
        if i % 5 == 0:
            type_salle = 'Amphi'
            capacite = 150 + (i * 10)
            salle = salles['Amphi'][i % len(salles['Amphi'])]
        elif i % 3 == 0:
            type_salle = 'Laboratoire'
            capacite = 30 + (i * 2)
            salle = salles['Laboratoire'][i % len(salles['Laboratoire'])]
        else:
            type_salle = 'Salle'
            capacite = 50 + (i * 5)
            salle = salles['Salle'][i % len(salles['Salle'])]

        # Nombre d'étudiants
        nb_etudiants = min(capacite, 30 + (i * 8))

        # Statut selon le remplissage
        taux_remplissage = nb_etudiants / capacite
        if taux_remplissage > 1:
            statut = 'CONFLIT'
        elif taux_remplissage > 0.9:
            statut = 'WARNING'
        else:
            statut = 'OK'

        # Professeur selon la spécialité
        profs_filtres = [
    p for p in professeurs if p['specialite'] == departement]
        if profs_filtres:
            prof = profs_filtres[i % len(profs_filtres)]
        else:
            prof = professeurs[i % len(professeurs)]

        examen = {
            'id_examen': i + 1000,
            'departement': departement,
            'formation': formation,
            'nom_module': module,
            'code_module': f"{departement[:3]}{i + 1:03d}",
            'date_exam': date_exam.strftime('%Y-%m-%d'),
            'heure_debut': heures[i % len(heures)],
            'duree': '2h' if i % 2 == 0 else '3h',
            'nom_salle': salle,
            'type_salle': type_salle,
            'professeur': f"Prof. {prof['nom']}",
            'prenom_professeur': prof['prenom'],
            'email_prof': f"{prof['prenom'].lower()}.{prof['nom'].lower()}@faculte.com",
            'capacite_salle': capacite,
            'nb_etudiants': nb_etudiants,
            'taux_remplissage': f"{taux_remplissage * 100:.1f}%",
            'statut': statut,
            'surveillant': f"Prof. {prof['nom']}",
            'matiere': module,
            'session': 'Principale' if i % 2 == 0 else 'Rattrapage',
            'coefficient': i % 3 + 1
        }
        planning.append(examen)

    return planning


def detecter_conflits(planning):
    """Détecte les conflits dans un planning"""
    conflits = []

    # Conflits de salles (même salle, même date, même heure)
    planning_par_salle = {}
    for examen in planning:
        cle = f"{
    examen['date_exam']}_{
        examen['heure_debut']}_{
            examen['nom_salle']}"
        if cle in planning_par_salle:
            conflit = {
                'type': 'SALLE',
                'severite': 'HAUTE',
                'message': f"Conflit de salle: {examen['nom_salle']} doublement réservée le {examen['date_exam']} à {examen['heure_debut']}",
                'examens': [planning_par_salle[cle], examen],
                'date': examen['date_exam'],
                'salle': examen['nom_salle']
            }
            conflits.append(conflit)
        else:
            planning_par_salle[cle] = examen

    # Conflits de professeurs
    planning_par_prof = {}
    for examen in planning:
        if examen.get('professeur'):
            cle = f"{
    examen['date_exam']}_{
        examen['heure_debut']}_{
            examen['professeur']}"
            if cle in planning_par_prof:
                conflit = {
                    'type': 'PROFESSEUR',
                    'severite': 'MOYENNE',
                    'message': f"Conflit de professeur: {examen['professeur']} a deux examens le {examen['date_exam']} à {examen['heure_debut']}",
                    'examens': [planning_par_prof[cle], examen],
                    'date': examen['date_exam'],
                    'professeur': examen['professeur']
                }
                conflits.append(conflit)
            else:
                planning_par_prof[cle] = examen

    # Surcapacité des salles
    for examen in planning:
        if examen['nb_etudiants'] > examen['capacite_salle']:
            conflit = {
                'type': 'CAPACITE',
                'severite': 'CRITIQUE',
                'message': f"Surcapacité: {examen['nom_salle']} (capacité: {examen['capacite_salle']}, étudiants: {examen['nb_etudiants']})",
                'examens': [examen],
                'date': examen['date_exam'],
                'salle': examen['nom_salle'],
                'capacite': examen['capacite_salle'],
                'etudiants': examen['nb_etudiants']
            }
            conflits.append(conflit)

    return conflits


def optimiser_ressources(planning, conflits):
    """Suggestions d'optimisation des ressources"""
    suggestions = []

    # Suggérer des salles alternatives pour les conflits
    salles_disponibles = [
        'Salle 301', 'Salle 302', 'Salle 303', 'Salle 401', 'Salle 402',
        'Amphi E', 'Amphi F', 'Lab Info C', 'Lab Physique 2'
    ]

    for conflit in conflits:
        if conflit['type'] == 'SALLE':
            for salle_alt in salles_disponibles:
                suggestion = {
                    'type': 'REAFFECTATION_SALLE',
                    'message': f"Suggérer la salle {salle_alt} pour l'examen du {conflit['date']} à la place de {conflit['salle']}",
                    'conflit': conflit,
                    'solution': salle_alt,
                    'gain': "Élimination du conflit de salle"
                }
                suggestions.append(suggestion)
                break

        elif conflit['type'] == 'CAPACITE':
            # Trouver une salle avec plus de capacité
            for salle_capacite in ['Amphi A', 'Amphi B', 'Amphi C']:
                suggestion = {
                    'type': 'CHANGEMENT_CAPACITE',
                    'message': f"Déplacer vers {salle_capacite} (capacité 200) pour résoudre la surcapacité",
                    'conflit': conflit,
                    'solution': salle_capacite,
                    'gain': f"Résolution surcapacité: {conflit['etudiants']} > {conflit['capacite']}"
                }
                suggestions.append(suggestion)
                break

    # Suggestions de répartition des horaires
    horaires_suggérés = ['08:30', '13:30', '15:30', '17:30']
    for i, examen in enumerate(planning):
        if i % 4 == 0:
            suggestion = {
                'type': 'REORGANISATION_HORAIRE',
                'message': f"Décaler l'examen de {examen['nom_module']} à {horaires_suggérés[i % len(horaires_suggérés)]}",
                'examen': examen,
                'nouvel_horaire': horaires_suggérés[i % len(horaires_suggérés)],
                'gain': "Meilleure répartition des créneaux"
            }
            suggestions.append(suggestion)

    return suggestions


def envoyer_email(destinataire, sujet, contenu_text, contenu_html=None):
    """Envoie un email (fonction de simulation)"""
    try:
        print(f"📧 Email simulé envoyé à: {destinataire}")
        print(f"📋 Sujet: {sujet}")
        print(f"📝 Contenu: {contenu_text[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur d'envoi d'email: {e}")
        return False


def exporter_csv(data, filename):
    """Exporte des données en CSV"""
    try:
        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')

        if data and len(data) > 0:
            # Écrire les en-têtes
            headers = data[0].keys()
            writer.writerow(headers)

            # Écrire les données
            for row in data:
                writer.writerow([str(row.get(h, '')) for h in headers])

        output.seek(0)
        return output.getvalue()
    except Exception as e:
        print(f"❌ Erreur d'export CSV: {e}")
        return None

# ==================== ROUTES PUBLIQUES ====================


@app.route('/', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        role = request.form.get('role', '').strip()

        if not username or not role:
            flash('Veuillez remplir tous les champs', 'danger')
            return render_template('interface.html')

        # Mode simulation (sans base de données)
        session['user'] = username
        session['role'] = role
        session['user_id'] = 1000 + hash(username) % 1000
        session['full_name'] = f"{username} Utilisateur"
        session['departement'] = 'Informatique' if role == 'etudiant' else 'Administration'
        session['email'] = f"{username.lower()}@faculte.com"

        # Messages de bienvenue
        messages_bienvenue = {
            'etudiant': 'Bienvenue dans votre espace étudiant !',
            'professeur': 'Bienvenue dans votre espace professeur !',
            'administrateur': 'Bienvenue dans l\'espace d\'administration !',
            'chef_departement': 'Bienvenue chef de département !',
            'doyen': 'Bienvenue Monsieur le Doyen !'
        }

        flash(messages_bienvenue.get(role, 'Bienvenue !'), 'success')

        # Redirection selon le rôle
        redirect_routes = {
            'etudiant': 'etudiant_dashboard',
            'professeur': 'professeur_dashboard',
            'administrateur': 'administrateur_dashboard',
            'chef_departement': 'chef_departement_dashboard',
            'doyen': 'doyen_dashboard'
        }

        return redirect(url_for(redirect_routes.get(role, 'login')))

    return render_template('interface.html')


@app.route('/logout')
def logout():
    """Déconnexion"""
    session.clear()
    flash('Vous avez été déconnecté avec succès', 'info')
    return redirect(url_for('login'))


@app.route('/test')
def test():
    """Route de test"""
    return jsonify({
        'status': 'OK',
        'message': 'Application EDT fonctionnelle',
        'timestamp': datetime.now().isoformat()
    })

# ==================== ROUTES ÉTUDIANT ====================


@app.route('/etudiant/dashboard')
@role_required('etudiant')
def etudiant_dashboard():
    """Tableau de bord étudiant"""
    # Statistiques simulées
    stats = {
        'total_examens': 6,
        'examens_prochains': 3,
        'examens_termines': 2,
        'moyenne': 14.5,
        'prochain_examen': (datetime.now() + timedelta(days=2)).strftime('%d/%m/%Y')
    }

    return render_template('etudiant.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         stats=stats)


@app.route('/etudiant/planning')
@role_required('etudiant')
def planning_etudiant():
    """Route alternative pour le planning étudiant"""
    return redirect(url_for('consulter_planning'))


@app.route('/etudiant/consulter_planning', methods=['GET', 'POST'])
@role_required('etudiant')
def consulter_planning():
    """Consultation du planning étudiant"""
    if request.method == 'POST':
        try:
            date_debut = request.form.get('date_debut', '')
            date_fin = request.form.get('date_fin', '')
            departement = request.form.get(
    'departement', session.get(
        'departement', 'Informatique'))

            if not date_debut:
                date_debut = datetime.now().strftime('%Y-%m-%d')

            planning = generer_planning_simule(date_debut, departement)

            if date_fin:
                try:
                    date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d')
                    planning = [e for e in planning
                              if datetime.strptime(e['date_exam'], '%Y-%m-%d') <= date_fin_obj]
                except ValueError:
                    flash('Format de date de fin invalide', 'warning')

            conflits = detecter_conflits(planning)

            # CORRECTION ICI : utiliser planning_etudiant.html au lieu de
            # consulter_planning.html
            return render_template('planning_etudiant.html',
                                 planning=planning,
                                 conflits=conflits,
                                 date_debut=date_debut,
                                 date_fin=date_fin,
                                 departement=departement,
                                 username=session.get('user'),
                                 full_name=session.get('full_name'),
                                 role=session.get('role'))

        except Exception as e:
            flash(
    f'Erreur lors de la génération du planning: {
        str(e)}', 'danger')
            return redirect(url_for('consulter_planning'))

    # GET request
    date_par_defaut = datetime.now().strftime('%Y-%m-%d')
    date_fin_par_defaut = (
    datetime.now() +
    timedelta(
        days=14)).strftime('%Y-%m-%d')

    # CORRECTION ICI : utiliser planning_etudiant.html au lieu de
    # consulter_planning.html
    return render_template('planning_etudiant.html',
                         date_debut=date_par_defaut,
                         date_fin=date_fin_par_defaut,
                         departement=session.get(
                             'departement', 'Informatique'),
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))


@app.route('/etudiant/examens')
@role_required('etudiant')
def examens_etudiant():
    """Liste des examens de l'étudiant"""
    examens = generer_planning_simule(datetime.now().strftime('%Y-%m-%d'),
                                     session.get(
    'departement', 'Informatique'),
                                     nb_jours=14)

    # Ajouter des notes simulées
    for i, examen in enumerate(examens):
        examen['note'] = 10 + (i % 11)  # Notes de 10 à 20
        examen['appreciation'] = ['Excellent', 'Très bien',
            'Bien', 'Assez bien', 'Passable'][i % 5]
        examen['date_publication'] = (
    datetime.now() +
    timedelta(
        days=i +
         5)).strftime('%d/%m/%Y')

    return render_template('examens.html',
                         examens=examens,
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))


@app.route('/etudiant/edt')
@role_required('etudiant')
def edt_etudiant():
    """Emploi du temps étudiant"""
    planning = generer_planning_simule(datetime.now().strftime('%Y-%m-%d'),
                                     session.get('departement', 'Informatique'))

    # Grouper par date pour l'affichage calendrier
    planning_par_date = {}
    for examen in planning:
        date_key = examen['date_exam']
        if date_key not in planning_par_date:
            planning_par_date[date_key] = []
        planning_par_date[date_key].append(examen)

    return render_template('edt_etudiants.html',
                         planning=planning,
                         planning_par_date=planning_par_date,
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))


@app.route('/etudiant/envoyer_rappels', methods=['GET', 'POST'])
@role_required('etudiant')
def envoyer_rappels():
    """Envoi de rappels par email"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        type_rappel = request.form.get('type_rappel', 'immédiat')

        if not email or '@' not in email:
            flash('Veuillez saisir une adresse email valide', 'danger')
            return redirect(url_for('envoyer_rappels'))

        # Récupérer le prochain examen
        planning = generer_planning_simule(datetime.now().strftime('%Y-%m-%d'),
                                         session.get('departement', 'Informatique'))

        if planning:
            prochain_examen = planning[0]

            # Préparer le contenu de l'email
            sujet = f"📅 Rappel d'examen - {prochain_examen['nom_module']}"

            contenu_text = f"""
            Bonjour {session.get('full_name')},

            Ceci est un rappel pour votre examen :

            📝 Matière: {prochain_examen['nom_module']}
            📅 Date: {prochain_examen['date_exam']}
            🕐 Heure: {prochain_examen['heure_debut']}
            🏫 Salle: {prochain_examen['nom_salle']}
            👨‍🏫 Professeur: {prochain_examen['professeur']}

            Conseils:
            • Présentez-vous 15 minutes avant
            • Apportez votre carte d'étudiant
            • Matériel autorisé: Calculatrice simple

            Bon courage !
            Service des Examens - Faculté des Sciences
            """

            # Envoyer l'email (simulation)
            succes = envoyer_email(email, sujet, contenu_text)

            if succes:
                flash('✅ Rappel envoyé avec succès !', 'success')
            else:
                flash('❌ Erreur lors de l\'envoi du rappel', 'danger')
        else:
            flash('Aucun examen à venir', 'info')

        return redirect(url_for('envoyer_rappels'))

    return render_template('confirmation_rappels.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))


@app.route('/etudiant/imprimer_planning', methods=['POST'])
@role_required('etudiant')
def imprimer_planning_etudiant():
    """Impression du planning étudiant"""
    try:
        date_debut = request.form.get(
    'date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = request.form.get(
    'departement', session.get(
        'departement', 'Informatique'))

        planning = generer_planning_simule(date_debut, departement)

        # Générer le HTML pour impression
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Planning des Examens - {session.get('full_name')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .info {{ margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .footer {{ margin-top: 50px; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📅 Planning des Examens</h1>
        <h3>Étudiant: {session.get('full_name')}</h3>
    </div>

    <div class="info">
        <p><strong>Département:</strong> {departement}</p>
        <p><strong>Période:</strong> {date_debut} au {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}</p>
        <p><strong>Généré le:</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
    </div>

    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Heure</th>
                <th>Matière</th>
                <th>Salle</th>
                <th>Professeur</th>
                <th>Durée</th>
            </tr>
        </thead>
        <tbody>"""

        for examen in planning:
            html_content += f"""
            <tr>
                <td>{examen['date_exam']}</td>
                <td>{examen['heure_debut']}</td>
                <td>{examen['nom_module']}</td>
                <td>{examen['nom_salle']}</td>
                <td>{examen['professeur']}</td>
                <td>{examen['duree']}</td>
            </tr>"""

        html_content += f"""
        </tbody>
    </table>

    <div class="footer">
        <p>Document généré automatiquement - Système EDT</p>
        <p>Faculté des Sciences • Service des Examens</p>
    </div>

    <script>
        window.onload = function() {{
            window.print();
            setTimeout(function() {{
                window.close();
            }}, 1000);
        }};
    </script>
</body>
</html>"""

        return html_content

    except Exception as e:
        return f"Erreur lors de l'impression: {str(e)}", 500


@app.route('/etudiant/export_csv')
@role_required('etudiant')
def export_csv_etudiant():
    """Export du planning en CSV"""
    try:
        planning = generer_planning_simule(datetime.now().strftime('%Y-%m-%d'),
                                         session.get('departement', 'Informatique'))

        csv_content = exporter_csv(
    planning, f"planning_{
        session.get('user')}_{
            datetime.now().strftime('%Y%m%d')}.csv")

        if csv_content:
            response = make_response(csv_content)
            response.headers["Content-Disposition"] = f"attachment; filename=planning_etudiant.csv"
            response.headers["Content-type"] = "text/csv; charset=utf-8"
            return response
        else:
            flash('Erreur lors de la génération du fichier CSV', 'danger')
            return redirect(url_for('etudiant_dashboard'))

    except Exception as e:
        flash(f'Erreur lors de l\'export CSV: {str(e)}', 'danger')
        return redirect(url_for('etudiant_dashboard'))

# ==================== ROUTES PROFESSEUR ====================


@app.route('/professeur/dashboard')
@role_required('professeur')
def professeur_dashboard():
    """Tableau de bord professeur"""
    stats = {
        'examens_a_surveiller': 8,
        'examens_corriges': 15,
        'moyenne_classe': 13.2,
        'prochaine_surveillance': (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
    }

    return render_template('professeur.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         stats=stats)


@app.route('/professeur/planning', methods=['GET', 'POST'])
@role_required('professeur')
def planning_professeur():
    """Planning des surveillances"""
    if request.method == 'POST':
        date_debut = request.form.get(
    'date_debut', datetime.now().strftime('%Y-%m-%d'))

        # Générer planning avec focus sur ce professeur
        planning = generer_planning_simule(date_debut, 'Informatique')

        # Filtrer pour les examens où ce professeur est surveillant
        planning_prof = [
    e for e in planning if e['professeur'] == f"Prof. {
        session.get('user')}"]

        return render_template('planning_professeur.html',
                             planning=planning_prof,
                             date_debut=date_debut,
                             username=session.get('user'),
                             full_name=session.get('full_name'),
                             role=session.get('role'))

    return render_template('planning_professeur.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

# ==================== ROUTES DOYEN ====================


@app.route('/doyen/dashboard')
@role_required('doyen')
def doyen_dashboard():
    """Tableau de bord doyen"""
    stats = {
        'total_departements': 5,
        'total_etudiants': 1250,
        'total_professeurs': 85,
        'examens_planifies': 120,
        'conflits_detectes': 3
    }

    return render_template('doyen_dashboard.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         stats=stats)


@app.route('/doyen/enseignants')
@role_required('doyen')
def doyen_enseignants():
    """Gestion des enseignants"""
    # Données simulées d'enseignants
    enseignants = []
    departements = [
    'Informatique',
    'Mathématiques',
    'Physique',
    'Chimie',
     'Biologie']

    for i in range(15):
        enseignants.append({
            'id': 2000 + i,
            'nom': f'Professeur{i + 1}',
            'prenom': f'Prénom{i + 1}',
            'departement': departements[i % len(departements)],
            'specialite': ['Informatique', 'Maths', 'Physique', 'Chimie', 'Biologie'][i % 5],
            'email': f'prof{i + 1}@faculte.com',
            'telephone': f'06 {i:02d} {i + 10:02d} {i + 20:02d} {i + 30:02d}',
            'statut': ['Titulaire', 'Vacataire', 'Contractuel'][i % 3],
            'heures': 192 + (i * 4)
        })

    return render_template('doyen_enseignants.html',
                         enseignants=enseignants,
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))


@app.route('/doyen/valider', methods=['GET', 'POST'])
@role_required('doyen')
def valider_edt():
    """Validation de l'EDT"""
    if request.method == 'POST':
        action = request.form.get('action')
        examen_id = request.form.get('examen_id')

        if action == 'valider':
            flash(f'✅ Examen {examen_id} validé avec succès', 'success')
        elif action == 'rejeter':
            flash(f'❌ Examen {examen_id} rejeté', 'warning')
        else:
            flash('Action non reconnue', 'danger')

    # Générer planning avec statuts de validation
    planning = generer_planning_simule(
    datetime.now().strftime('%Y-%m-%d'), 'Informatique')

    for examen in planning:
        examen['valide_par'] = 'Non validé'
        examen['date_validation'] = ''
        if int(examen['id_examen']) % 3 == 0:
            examen['valide_par'] = 'Doyen'
            examen['date_validation'] = (
    datetime.now() -
    timedelta(
        days=2)).strftime('%d/%m/%Y')

    return render_template('valider_edt.html',
                         planning=planning,
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

# ==================== ROUTES ADMINISTRATEUR ====================


@app.route('/administrateur/dashboard')
@role_required('administrateur')
def administrateur_dashboard():
    """Tableau de bord administrateur"""
    stats = {
        'total_utilisateurs': 450,
        'examens_planifies': 85,
        'conflits_resolus': 12,
        'salles_utilisees': 25,
        'exportations': 47
    }

    return render_template('administrateur.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         stats=stats)


@app.route('/administrateur')
def redirect_administrateur():
    """Redirection vers le dashboard administrateur"""
    return redirect(url_for('administrateur_dashboard'))


@app.route('/administrateur/generer', methods=['GET', 'POST'])
@role_required('administrateur')
def generer_edt():
    """Génération de l'EDT"""
    if request.method == 'POST':
        date_debut = request.form.get('date_debut', '')
        departement = request.form.get('departement', 'Informatique')

        if not date_debut:
            flash('Veuillez sélectionner une date de début', 'warning')
            return redirect(url_for('generer_edt'))

        # Générer le planning
        planning = generer_planning_simule(date_debut, departement)

        # Détecter les conflits
        conflits = detecter_conflits(planning)

        # Calculer les statistiques
        stats = {
            'total_examens': len(planning),
            'conflits': len(conflits),
            'salles_utilisees': len(set(e['nom_salle'] for e in planning)),
            'professeurs': len(set(e['professeur'] for e in planning))
        }

        flash(
    f'✅ EDT généré pour {departement} avec {
        len(planning)} examens',
         'success')

        return render_template('generer_edt.html',
                             planning=planning,
                             conflits=conflits,
                             stats=stats,
                             date_debut=date_debut,
                             departement=departement,
                             username=session.get('user'),
                             full_name=session.get('full_name'),
                             role=session.get('role'))

    return render_template('generer_edt.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))


@app.route('/administrateur/export_csv', methods=['POST'])
@role_required('administrateur')
def export_csv_admin():
    """Export CSV de l'EDT"""
    try:
        date_debut = request.form.get(
    'date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = request.form.get('departement', 'Informatique')

        planning = generer_planning_simule(date_debut, departement)
        csv_content = exporter_csv(
    planning, f"edt_{departement}_{date_debut}.csv")

        if csv_content:
            response = make_response(csv_content)
            response.headers[
    "Content-Disposition"] = f"attachment; filename=edt_{departement}_{date_debut}.csv"
            response.headers["Content-type"] = "text/csv; charset=utf-8"
            return response
        else:
            flash('Erreur lors de la génération du CSV', 'danger')
            return redirect(url_for('generer_edt'))

    except Exception as e:
        flash(f'Erreur lors de l\'export CSV: {str(e)}', 'danger')
        return redirect(url_for('generer_edt'))


@app.route('/administrateur/imprimer_planning', methods=['POST'])
@role_required('administrateur')
def imprimer_planning_admin():
    """Impression du planning"""
    try:
        date_debut = request.form.get(
    'date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = request.form.get('departement', 'Informatique')

        planning = generer_planning_simule(date_debut, departement)

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Planning EDT - {departement}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #000; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
        .footer {{ margin-top: 50px; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>EMPLOI DU TEMPS - {departement}</h1>
        <p>Date: {date_debut} | Généré le: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>

    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Heure</th>
                <th>Module</th>
                <th>Salle</th>
                <th>Type</th>
                <th>Professeur</th>
                <th>Capacité</th>
                <th>Étudiants</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>"""

        for examen in planning:
            html_content += f"""
            <tr>
                <td>{examen['date_exam']}</td>
                <td>{examen['heure_debut']}</td>
                <td>{examen['nom_module']}</td>
                <td>{examen['nom_salle']}</td>
                <td>{examen['type_salle']}</td>
                <td>{examen['professeur']}</td>
                <td>{examen['capacite_salle']}</td>
                <td>{examen['nb_etudiants']}</td>
                <td>{examen['statut']}</td>
            </tr>"""

        html_content += """</tbody>
    </table>

    <div class="footer">
        <p>Document officiel - Service des Examens</p>
    </div>

    <script>
        window.onload = function() {{
            window.print();
        }}
    </script>
</body>
</html>"""

        return html_content

    except Exception as e:
        return f"Erreur d'impression: {str(e)}", 500
@app.route('/administrateur/conflits', methods=['GET', 'POST'])
@role_required('administrateur')
def detecter_conflits_route():
    """Détection des conflits"""
    print(f"=== DETECTER CONFLITS ROUTE ===")
    print(f"Méthode: {request.method}")
    print(f"Form data: {dict(request.form)}")
    print(f"Session: {session}")

    if request.method == 'POST':
        date_debut = request.form.get('date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = request.form.get('departement', 'Informatique')
    print(f"Date début reçue: {date_debut}")
    print(f"Département reçu: {departement}")

        planning = generer_planning_simule(date_debut, departement)
        conflits = detecter_conflits(planning)

    print(f"Nombre de conflits détectés: {len(conflits)}")

        flash(f'✅ {len(conflits)} conflits détectés', 'info' if not conflits else 'warning')

        return render_template('detecter_conflits.html',
                     conflits=conflits,
                     detection_lancee=True,  # AJOUTE CETTE LIGNE
                     date_debut=date_debut,
                     departement=departement,
                     username=session.get('user'),
                     full_name=session.get('full_name'),
                     role=session.get('role'))
    # GET request - afficher le formulaire
    return render_template('detecter_conflits.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))
@app.route('/administrateur/lancer_detection_conflits', methods=['POST'])
@role_required('administrateur')
def lancer_detection_conflits():
    """Lancer la détection des conflits"""
    date_debut = request.form.get('date_debut', datetime.now().strftime('%Y-%m-%d'))
    departement = request.form.get('departement', 'Informatique')

    planning = generer_planning_simule(date_debut, departement)
    conflits = detecter_conflits(planning)

    flash(f'✅ Détection terminée : {len(conflits)} conflits trouvés', 'success' if len(conflits) == 0 else 'warning')

    return redirect(url_for('detecter_conflits_route'))

@app.route('/administrateur/optimiser', methods=['GET', 'POST'])
@role_required('administrateur')
def optimiser_ressources_route():
    """Optimisation des ressources"""
    print(f"=== DEBUG OPTIMISER RESSOURCES ===")
    print(f"Method: {request.method}")
    print(f"Form data: {request.form}")
    print(f"========================")

    if request.method == 'POST':
        date_debut = request.form.get('date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = request.form.get('departement', 'Informatique')

        planning = generer_planning_simule(date_debut, departement)
        conflits = detecter_conflits(planning)
        suggestions = optimiser_ressources(planning, conflits)

        flash(f'✅ {len(suggestions)} suggestions d\'optimisation', 'success')

        return render_template('optimiser_ressources.html',
                             planning=planning,
                             conflits=conflits,
                             suggestions=suggestions,
                             date_debut=date_debut,
                             departement=departement,
                             username=session.get('user'),
                             full_name=session.get('full_name'),
                             role=session.get('role'))

    return render_template('optimiser_ressources.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

@app.route('/administrateur/lancer_optimisation', methods=['POST'])
@role_required('administrateur')
def lancer_optimisation():
    """Lancer l'optimisation"""
    date_debut = request.form.get('date_debut', datetime.now().strftime('%Y-%m-%d'))
    departement = request.form.get('departement', 'Informatique')

    planning = generer_planning_simule(date_debut, departement)
    conflits = detecter_conflits(planning)
    suggestions = optimiser_ressources(planning, conflits)

    flash(f'✅ Optimisation terminée : {len(suggestions)} suggestions générées', 'success')

    return redirect(url_for('optimiser_ressources_route'))

@app.route('/administrateur/consulter_planning', methods=['GET', 'POST'])
@role_required('administrateur')
def consulter_planning_admin():
    """Consultation planning administrateur"""
    if request.method == 'POST':
        date_debut = request.form.get('date_debut', '')
        date_fin = request.form.get('date_fin', '')
        departement = request.form.get('departement', 'Tous')

        if not date_debut:
            date_debut = datetime.now().strftime('%Y-%m-%d')

        # Générer planning pour tous les départements ou un spécifique
        if departement == 'Tous':
            planning = []
            for dept in ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 'Biologie']:
                planning += generer_planning_simule(date_debut, dept, nb_jours=3)
        else:
            planning = generer_planning_simule(date_debut, departement)

        # Filtrer par date de fin
        if date_fin:
            try:
                date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d')
                planning = [e for e in planning
                          if datetime.strptime(e['date_exam'], '%Y-%m-%d') <= date_fin_obj]
            except ValueError:
                pass

        return render_template('consulter_planning_admin.html',
                             planning=planning,
                             date_debut=date_debut,
                             date_fin=date_fin,
                             departement=departement,
                             username=session.get('user'),
                             full_name=session.get('full_name'),
                             role=session.get('role'))

    date_par_defaut = datetime.now().strftime('%Y-%m-%d')
    date_fin_par_defaut = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    return render_template('consulter_planning_admin.html',
                         date_debut=date_par_defaut,
                         date_fin=date_fin_par_defaut,
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

# ==================== ROUTES CHEF DÉPARTEMENT ====================
@app.route('/chef_departement/dashboard')
@role_required('chef_departement')
def chef_departement_dashboard():
    """Tableau de bord chef de département"""
    stats = {
        'total_etudiants': 250,
        'total_professeurs': 18,
        'examens_departement': 35,
        'conflits_departement': 2,
        'moyenne_departement': 12.8
    }

    return render_template('chef_departement.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         stats=stats)

@app.route('/chef_departement')
def redirect_chef_departement():
    """Redirection vers le dashboard chef de département"""
    return redirect(url_for('chef_departement_dashboard'))

@app.route('/chef_departement/planning', methods=['GET', 'POST'])
@role_required('chef_departement')
def planning_chef_departement():
    """Planning du département"""
    if request.method == 'POST':
        date_debut = request.form.get('date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = session.get('departement', 'Informatique')

        planning = generer_planning_simule(date_debut, departement)
        conflits = detecter_conflits(planning)

        return render_template('planning_chef_departement.html',
                             planning=planning,
                             conflits=conflits,
                             date_debut=date_debut,
                             departement=departement,
                             username=session.get('user'),
                             full_name=session.get('full_name'),
                             role=session.get('role'))

    departement = session.get('departement', 'Informatique')
    date_par_defaut = datetime.now().strftime('%Y-%m-%d')

    return render_template('planning_chef_departement.html',
                         date_debut=date_par_defaut,
                         departement=departement,
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

# ==================== ROUTES COMMUNES ====================
@app.route('/profile')
@login_required
def profile():
    """Profil utilisateur"""
    user_info = {
        'username': session.get('user'),
        'full_name': session.get('full_name'),
        'role': session.get('role'),
        'user_id': session.get('user_id'),
        'departement': session.get('departement', 'Non spécifié'),
        'email': session.get('email', 'Non spécifié'),
        'date_inscription': (datetime.now() - timedelta(days=365)).strftime('%d/%m/%Y'),
        'derniere_connexion': datetime.now().strftime('%d/%m/%Y %H:%M')
    }

    return render_template('profile.html',
                         user=user_info,
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

@app.route('/a_propos')
def a_propos():
    """Page À propos"""
    return render_template('a_propos.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

@app.route('/contact')
def contact():
    """Page Contact"""
    return render_template('contact.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'))

# ==================== ROUTES AJAX/API ====================
@app.route('/api/planning')
@login_required
def api_planning():
    """API pour récupérer le planning"""
    try:
        date_debut = request.args.get('date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = request.args.get('departement', 'Informatique')

        planning = generer_planning_simule(date_debut, departement)

        return jsonify({
            'success': True,
            'planning': planning,
            'count': len(planning),
            'date_debut': date_debut,
            'departement': departement
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conflits')
@login_required
def api_conflits():
    """API pour détecter les conflits"""
    try:
        date_debut = request.args.get('date_debut', datetime.now().strftime('%Y-%m-%d'))
        departement = request.args.get('departement', 'Informatique')

        planning = generer_planning_simule(date_debut, departement)
        conflits = detecter_conflits(planning)

        return jsonify({
            'success': True,
            'conflits': conflits,
            'count': len(conflits),
            'date_debut': date_debut,
            'departement': departement
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== GESTION D'ERREURS ====================
@app.errorhandler(404)
def page_not_found(e):
    """Page 404"""
    return render_template('404.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Page 500"""
    return render_template('500.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         error=str(e)), 500

@app.errorhandler(403)
def forbidden(e):
    """Page 403"""
    return render_template('403.html',
                         username=session.get('user'),
                         full_name=session.get('full_name'),
                         role=session.get('role'),
                         error=str(e)), 403

# ==================== ROUTES DE DEBUG ====================
@app.route('/debug/session')
def debug_session():
    """Debug de la session"""
    return jsonify(dict(session))

@app.route('/debug/planning')
def debug_planning():
    """Debug du planning"""
    planning = generer_planning_simule(datetime.now().strftime('%Y-%m-%d'), 'Informatique')
    return jsonify(planning)

# ==================== MAIN ====================
if __name__ == '__main__':
    # Configuration pour PythonAnywhere
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    print(f"""
    ╔══════════════════════════════════════════════════════╗
    ║  🚀 Système EDT - Faculté des Sciences               ║
    ║  📅 Gestion des Emplois du Temps d'Examens           ║
    ║  👥 Rôles: Étudiant, Professeur, Admin, Chef, Doyen ║
    ║  🌐 URL: http://localhost:{port}                     ║
    ║  ⚙️  Mode: {'Debug' if debug else 'Production'}                ║
    ╚══════════════════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
