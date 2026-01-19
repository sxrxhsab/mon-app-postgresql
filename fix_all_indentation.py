#!/usr/bin/env python3
"""
Script pour corriger toutes les indentations en remplaçant les tabulations par 4 espaces
et en uniformisant l'indentation.
"""

import os

def fix_indentation(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Si la ligne commence par des tabulations, les remplacer par 4 espaces
        if line.startswith('\t'):
            # Compter le nombre de tabulations en début de ligne
            tab_count = 0
            for char in line:
                if char == '\t':
                    tab_count += 1
                else:
                    break
            # Remplacer chaque tabulation par 4 espaces
            new_line = ('    ' * tab_count) + line[tab_count:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    # Écrire le fichier corrigé
    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    
    print(f"✅ Fichier {filepath} réindenté (tabulations remplacées)")

if __name__ == '__main__':
    fix_indentation('app.py')
