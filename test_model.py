import joblib
import pandas as pd

# =====================
# LOAD MODEL
# =====================
model = joblib.load("models/best_model.pkl")

# =====================
# TEST DATA
# =====================
test_house = {
    "surface": 160,
    "chambres": 3,
    "salles_de_bain": 2,
    "kitchen": 1,
    "etage": 5,
    "annee": 2016,
    "localisation": "Casablanca",
    "piscine": 1,
    "garage": 1,
    "balcon": 1,
    "terrasse": 0,
    "parking": 1,
    "gardien": 0,
    "ascenseur": 1,
    "jardin": 0,
    "belle_vue": 1
}

# =====================
# PREDICTION
# =====================
df = pd.DataFrame([test_house])

pred = model.predict(df)[0]

# =====================
# RESULT
# =====================
print("\n====================")
print("🧪 MODEL TEST")
print("====================")
print(f"Predicted Price: {int(pred):,} DH")