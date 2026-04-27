import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score, mean_absolute_error

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("Data/processed/clean_house_prediction_dataset.csv")

X = df.drop("prix_DH", axis=1)
y = df["prix_DH"]

# =====================
# SPLIT
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================
# PREPROCESS
# =====================
cat_cols = ["localisation"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
], remainder="passthrough")

# =====================
# MODELS
# =====================
models = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(),
    "XGBoost": XGBRegressor(n_estimators=200, random_state=42)
}

results = {}
best_model = None
best_score = -1

# =====================
# TRAIN LOOP
# =====================
for name, model in models.items():

    pipe = Pipeline([
        ("prep", preprocessor),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)

    r2 = r2_score(y_test, pred)
    mae = mean_absolute_error(y_test, pred)

    results[name] = (r2, mae)

    print(f"\n{name}")
    print("R2:", r2)
    print("MAE:", mae)

    # best model
    if r2 > best_score:
        best_score = r2
        best_model = pipe
        best_name = name

# =====================
# SAVE BEST MODEL
# =====================
joblib.dump(best_model, "models/best_model.pkl")

print("\n====================")
print("🏆 BEST MODEL:", best_name)
print("Saved → models/best_model.pkl")
print("====================")