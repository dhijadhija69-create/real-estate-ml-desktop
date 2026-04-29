# 🚀 COMMENT LANCER L'APPLICATION

## ⚡ Méthode la Plus Simple

### Windows (PowerShell)
```powershell
# 1. Ouvrir PowerShell dans le dossier du projet
# 2. Taper:
.\run.ps1
```

### Windows (Command Prompt / Batch)
```cmd
# 1. Ouvrir Command Prompt dans le dossier du projet
# 2. Taper:
python run.py

# OU double-cliquer sur run.bat
```

### macOS / Linux
```bash
# 1. Ouvrir Terminal dans le dossier du projet
# 2. Taper:
python run.py
```

---

## ✅ Avant de Lancer

Assurez-vous que le **virtual environment** est activé:

### Windows
```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux
```bash
source .venv/bin/activate
```

---

## 🔍 Vérifier la Configuration (IMPORTANT!)

Avant de lancer, exécutez cette commande pour vérifier que tout est OK:

```bash
python check_setup.py
```

Vous devriez voir:
```
✓ app/main.py                           (Point d'entrée de l'application)
✓ app/prediction.py                     (Module de prédiction)
✓ app/best_model.pkl                    (Modèle XGBoost)
✓ PyQt6                                 installé
✓ joblib                                installé
✓ numpy                                 installé
✓ pandas                                installé
```

Si vous voyez des `✗`, lisez la section "❌ Dépannage".

---

## ✨ L'Application Est Prête!

Une fois lancée, vous verrez:
1. 🎬 **Écran de démarrage** avec animation
2. 🔐 **Écran de connexion/inscription**
3. 🏠 **Interface de prédiction** pour estimer le prix d'une propriété

---

## ❌ Dépannage

### Erreur: "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Erreur: "best_model.pkl not found"
- Vérifiez que le fichier existe: `app/best_model.pkl`
- Exécutez: `python check_setup.py`

### Erreur: "No module named 'app'"
- Utilisez `python run.py` depuis la **racine** du projet
- OU naviguez à `app/` et faites `python main.py`

### Virtual environment n'est pas activé
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

---

## 📚 Autres Commandes Utiles

### Vérifier l'installation des dépendances
```bash
pip list
```

### Réinstaller les dépendances
```bash
pip install -r requirements.txt
```

### Voir les erreurs détaillées
```bash
python -c "from app.main import main; main()"
```

---

## 💡 Conseils

- Gardez le **virtual environment** activé
- Lancez toujours depuis la **racine** du projet
- Utilisez `python run.py` pour plus de stabilité

---

**Bon usage! 🎉**
