import re

with open('app.py', 'r') as f:
    lines = f.readlines()

# Niveau d'indentation actuel
current_indent = 0
indent_size = 4
new_lines = []

for i, line in enumerate(lines):
    # Compter les espaces en début de ligne
    stripped = line.lstrip()
    leading_spaces = len(line) - len(stripped)
    
    # Si c'est une ligne de décorateur pour une fonction, elle devrait être au même niveau que la fonction
    if stripped.startswith('@'):
        # Chercher la fonction suivante
        for j in range(i+1, min(i+5, len(lines))):
            if lines[j].strip().startswith('def '):
                # Aligner avec la fonction
                func_indent = len(lines[j]) - len(lines[j].lstrip())
                new_line = ' ' * func_indent + stripped
                lines[i] = new_line
                break
    
    # Pour les lignes de fonction, s'assurer qu'elles ont au moins un niveau d'indentation
    elif stripped.startswith('def ') or stripped.startswith('class '):
        if leading_spaces == 0:
            lines[i] = line  # Garder tel quel si c'est au niveau racine

with open('app.py', 'w') as f:
    f.writelines(lines)

print("✅ Fichier corrigé")
