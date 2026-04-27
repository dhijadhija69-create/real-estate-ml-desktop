import numpy as np
import pandas as pd
import joblib

# =====================
# load model
# =====================
model = joblib.load("models/xgboost_model.pkl")

# =====================
# prediction function
# =====================
def predict_price(data):
    df = pd.DataFrame([data])

    # feature engineering (نفس training)
    df["age_bien"] = 2024 - df["annee"]

    equip = ["piscine","garage","balcon","terrasse","parking",
             "gardien","ascenseur","jardin","belle_vue"]

    df["nb_equipements"] = df[equip].sum(axis=1)

    # prediction
    price = model.predict(df)[0]

    return price


# =====================
# test
# =====================
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

price = predict_price(house)

print("🏠 Price:", int(price), "DH")