import numpy as np
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "..", "models", "best_model.pkl")

model = joblib.load(model_path)


def predict_price(data):
    df = pd.DataFrame([data])

    # feature engineering (important same training)
    df["age_bien"] = 2026 - df["annee"]

    equip = ["piscine","garage","balcon","terrasse","parking",
             "gardien","ascenseur","jardin","belle_vue"]

    df["nb_equipements"] = df[equip].sum(axis=1)

    return model.predict(df)[0]


house = {
    "surface": 150,
    "chambres": 3,
    "salles_de_bain": 2,
    "kitchen": 1,
    "etage": 5,
    "annee": 2015,
    "localisation": "Marrakech",
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

print("🏠 Price:", int(predict_price(house)), "DH")
