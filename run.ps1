# Script PowerShell pour lancer l'application
# Usage: .\run.ps1

# Vérifier que le venv est activé
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activation du virtual environment..." -ForegroundColor Yellow
    & ".\.venv\Scripts\Activate.ps1"
}

# Vérifier la configuration
Write-Host "`nVérification de la configuration..." -ForegroundColor Cyan
python check_setup.py

# Lancer l'application
Write-Host "`nLancement de l'application..." -ForegroundColor Green
python run.py
