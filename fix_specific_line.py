#!/usr/bin/env python3
# Corriger spécifiquement la ligne 1142

with open('app.py', 'r') as f:
    lines = f.readlines()

# La ligne 1142 (index 1141 dans la liste) doit être alignée avec les autres décorateurs
# Regardons les lignes avant pour trouver le bon niveau d'indentation
if len(lines) > 1141:
    # Chercher la dernière ligne avec un décorateur avant la ligne 1142
    for i in range(1140, 1100, -1):
        if i < len(lines) and '@app.route' in lines[i]:
            # Copier l'indentation de cette ligne
            import re
            match = re.match(r'^(\s*)', lines[i])
            if match:
                indent = match.group(1)
                # Appliquer cette indentation à la ligne 1142
                lines[1141] = indent + lines[1141].lstrip()
                break
    
    # Écrire le fichier corrigé
    with open('app.py', 'w') as f:
        f.writelines(lines)
    print("✅ Ligne 1142 corrigée")
