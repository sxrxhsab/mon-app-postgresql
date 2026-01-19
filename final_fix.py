with open('app.py', 'r') as f:
    content = f.read()

# Remplacer le bloc problématique
# Trouver la ligne avec @app.route('/administrateur/conflits'
lines = content.split('\n')
for i in range(len(lines)):
    if '@app.route(\'/administrateur/conflits\' in lines[i]:
        # Supprimer toute indentation au début
        lines[i] = lines[i].lstrip()
        # Vérifier la ligne suivante (@role_required)
        if i+1 < len(lines) and '@role_required' in lines[i+1]:
            lines[i+1] = lines[i+1].lstrip()
        break

# Réassembler
with open('app.py', 'w') as f:
    f.write('\n'.join(lines))
print("✅ Correction appliquée")
