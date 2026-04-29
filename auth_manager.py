"""
auth/auth_manager.py - Authentication System
Uses users.csv in data/ folder
"""

import csv, uuid, hashlib, re, os
from datetime import datetime
from typing import Tuple, Optional, Dict

try:
    import bcrypt
    USE_BCRYPT = True
except ImportError:
    USE_BCRYPT = False

BASE_DIR   = os.path.join(os.path.dirname(__file__), "..")
USERS_CSV  = os.path.join(BASE_DIR, "data", "users.csv")
COLUMNS    = ["id", "username", "email", "password_hash", "created_at"]


def _ensure_csv():
    os.makedirs(os.path.dirname(USERS_CSV), exist_ok=True)
    if not os.path.isfile(USERS_CSV):
        with open(USERS_CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=COLUMNS).writeheader()


class AuthManager:

    def __init__(self):
        _ensure_csv()

    def signup(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        username, email, password = username.strip(), email.strip().lower(), password.strip()

        if not username or len(username) < 2:
            return False, "Le nom doit avoir au moins 2 caractères."
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            return False, "Email invalide."
        if len(password) < 6:
            return False, "Le mot de passe doit avoir au moins 6 caractères."
        if self._find(email):
            return False, "Un compte avec cet email existe déjà."

        with open(USERS_CSV, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=COLUMNS).writerow({
                "id":            str(uuid.uuid4())[:8],
                "username":      username,
                "email":         email,
                "password_hash": self._hash(password),
                "created_at":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
        return True, f"Compte créé ! Bienvenue, {username}."

    def login(self, email: str, password: str) -> Tuple[bool, Optional[Dict]]:
        email, password = email.strip().lower(), password.strip()
        user = self._find(email)
        if not user or not self._verify(password, user["password_hash"]):
            return False, None
        return True, user

    def _find(self, email: str) -> Optional[Dict]:
        try:
            with open(USERS_CSV, "r", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row["email"].lower() == email:
                        return row
        except FileNotFoundError:
            pass
        return None

    def _hash(self, pw: str) -> str:
        if USE_BCRYPT:
            return bcrypt.hashpw(pw.encode(), bcrypt.gensalt(rounds=12)).decode()
        salt   = os.urandom(16).hex()
        digest = hashlib.sha256((salt + pw).encode()).hexdigest()
        return f"sha256:{salt}:{digest}"

    def _verify(self, pw: str, stored: str) -> bool:
        if USE_BCRYPT and not stored.startswith("sha256:"):
            return bcrypt.checkpw(pw.encode(), stored.encode())
        try:
            _, salt, digest = stored.split(":")
            return hashlib.sha256((salt + pw).encode()).hexdigest() == digest
        except ValueError:
            return False
