#!/usr/bin/env python3
# Script pour corriger l'indentation

import re

def fix_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Nettoyer l'indentation : remplacer les tabulations par 4 espaces
    for i in range(len(lines)):
        # Compter le nombre d'espaces/tabulations au début
        line = lines[i]
        if line.startswith('    '):
            # Remplacer 4 espaces par 4 espaces (ne rien faire)
            pass
        elif line.startswith('\t'):
            # Remplacer les tabulations par 4 espaces
            lines[i] = line.replace('\t', '    ', 1)
    
    # Écrire le fichier corrigé
    with open(filename, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Fichier {filename} réindenté")

if __name__ == '__main__':
    fix_file('app.py')
