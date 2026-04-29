# Comment Exécuter l'Application

## Méthode 1: Depuis la racine du projet (RECOMMANDÉ)

```bash
# Depuis le répertoire racine du projet (real-estate-ml-desktop)
python run.py
```

Ou sous Windows, double-cliquez sur:
```
run.bat
```

## Méthode 2: Depuis le répertoire app

```bash
# Naviguer au répertoire app
cd app

# Exécuter main.py
python main.py
```

## Prérequis

1. **Python 3.8+** doit être installé
2. **Virtual Environment** doit être activé:
   ```bash
   # Activation sur Windows
   .\.venv\Scripts\activate
   
   # Activation sur macOS/Linux
   source .venv/bin/activate
   ```

3. **Dépendances** doivent être installées:
   ```bash
   pip install -r requirements.txt
   ```

## Fichiers Importants

- `run.py` - Script de lancement depuis la racine du projet (NOUVEAU)
- `app/main.py` - Point d'entrée de l'application
- `app/best_model.pkl` - Modèle XGBoost pour les prédictions
- `app/data/users.csv` - Base de données des utilisateurs

## Fonctionnalités

1. **Inscription/Connexion** - Créer un compte ou se connecter
2. **Prédiction** - Remplir les détails d'une propriété et obtenir une estimation de prix
3. **Interface Moderne** - UI élégante avec PyQt6

## Dépannage

**Erreur: "No module named 'app'"**
- Assurez-vous d'exécuter l'application depuis la racine avec `python run.py`
- Ou naviguer à `app/` et exécuter `python main.py`

**Erreur: "No module named 'best_model.pkl'"**
- Le fichier modèle doit être dans `app/best_model.pkl`
- Vérifiez que le fichier existe avec la commande: `ls app/best_model.pkl`

**Erreur: PyQt6 non installé**
- Réinstallez les dépendances: `pip install -r requirements.txt`
