#!/usr/bin/env python3
"""
check_setup.py - Vérifier que tout est configuré correctement
==============================================================
Vérifie que tous les fichiers nécessaires existent et que les imports fonctionnent.
"""

import os
import sys

def check_files():
    """Vérifier que tous les fichiers nécessaires existent"""
    
    root = os.path.dirname(os.path.abspath(__file__))
    print("Répertoire racine du projet:", root)
    print()
    
    required_files = [
        ("app/main.py", "Point d'entrée de l'application"),
        ("app/prediction.py", "Module de prédiction"),
        ("app/best_model.pkl", "Modèle XGBoost"),
        ("app/ui/splash_screen.py", "Écran de démarrage"),
        ("app/ui/login_window.py", "Écran de connexion"),
        ("app/ui/main_window.py", "Interface principale"),
        ("app/auth/auth_manager.py", "Système d'authentification"),
        ("requirements.txt", "Dépendances du projet"),
        (".venv", "Virtual environment"),
    ]
    
    print("✓ Vérification des fichiers:")
    print("-" * 60)
    
    all_exist = True
    for file_path, description in required_files:
        full_path = os.path.join(root, file_path)
        exists = os.path.exists(full_path)
        status = "✓" if exists else "✗"
        all_exist = all_exist and exists
        print(f"{status} {file_path:<35} ({description})")
    
    print()
    return all_exist

def check_imports():
    """Vérifier que les imports principaux fonctionnent"""
    
    print("✓ Vérification des imports:")
    print("-" * 60)
    
    imports = [
        ("PyQt6", "PyQt6.QtWidgets"),
        ("joblib", "joblib"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
    ]
    
    all_ok = True
    for package, module in imports:
        try:
            __import__(module)
            print(f"✓ {package:<20} installé")
        except ImportError as e:
            print(f"✗ {package:<20} NON INSTALLÉ - {e}")
            all_ok = False
    
    print()
    return all_ok

def main():
    print("=" * 60)
    print("VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 60)
    print()
    
    files_ok = check_files()
    imports_ok = check_imports()
    
    print("=" * 60)
    if files_ok and imports_ok:
        print("✓ TOUT EST OK! Vous pouvez lancer: python run.py")
    else:
        print("✗ Des problèmes ont été détectés.")
        if not imports_ok:
            print("   → Installez les dépendances: pip install -r requirements.txt")
        if not files_ok:
            print("   → Certains fichiers manquent.")
    print("=" * 60)

if __name__ == "__main__":
    main()
