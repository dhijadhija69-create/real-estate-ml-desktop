"""
Overfitting Detection Script - Moroccan Housing Price Prediction
Analyzes trained models for overfitting by comparing train vs test performance
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

def check_overfitting(model, X_train, y_train, X_test, y_test, model_name="Model"):
    """
    Function to detect overfitting by comparing train vs test performance
    """

    # =========================
    # 🔵 TRAIN PERFORMANCE
    # =========================
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_rmse = np.sqrt(np.mean((y_train - y_train_pred) ** 2))

    # =========================
    # 🔴 TEST PERFORMANCE
    # =========================
    y_test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, y_test_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_rmse = np.sqrt(np.mean((y_test - y_test_pred) ** 2))

    # =========================
    # 📊 RESULTS
    # =========================
    print("\n" + "="*70)
    print(f"📊 OVERFITTING CHECK - {model_name}")
    print("="*70)

    print(f"\n🔵 TRAIN PERFORMANCE:")
    print(f"   R² Score: {train_r2:.4f}")
    print(f"   MAE:      ${train_mae:>12,.2f}")
    print(f"   RMSE:     ${train_rmse:>12,.2f}")

    print(f"\n🔴 TEST PERFORMANCE:")
    print(f"   R² Score: {test_r2:.4f}")
    print(f"   MAE:      ${test_mae:>12,.2f}")
    print(f"   RMSE:     ${test_rmse:>12,.2f}")

    # =========================
    # 🚨 INTERPRETATION
    # =========================
    r2_gap = train_r2 - test_r2
    mae_gap = train_mae - test_mae
    rmse_gap = train_rmse - test_rmse

    print("\n" + "-"*70)
    print("📌 OVERFITTING ANALYSIS:")
    print("-"*70)
    print(f"   R² Gap (Train - Test):   {r2_gap:+.4f}")
    print(f"   MAE Gap (Train - Test):  ${mae_gap:+12,.2f}")
    print(f"   RMSE Gap (Train - Test): ${rmse_gap:+12,.2f}")

    print("\n" + "-"*70)
    print("✅ VERDICT:")
    print("-"*70)

    if r2_gap < 0.02:
        status = "✅ EXCELLENT - No significant overfitting"
        severity = "GOOD"
    elif r2_gap < 0.05:
        status = "⚠️ ACCEPTABLE - Slight overfitting possible"
        severity = "MILD"
    elif r2_gap < 0.10:
        status = "⚠️ WARNING - Moderate overfitting detected"
        severity = "MODERATE"
    else:
        status = "🚨 CRITICAL - Strong overfitting detected"
        severity = "SEVERE"
    
    print(f"   {status}")
    print("="*70)

    return {
        'model_name': model_name,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'r2_gap': r2_gap,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'mae_gap': mae_gap,
        'severity': severity
    }

def main():
    """Main overfitting check pipeline"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "🔍 OVERFITTING DETECTION - XGBOOST MODEL".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    try:
        # Load data
        print("\n📂 Loading dataset...")
        df = pd.read_csv("../Data/processed/clean_house_prediction_dataset.csv")
        print(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")

        # Prepare features and target
        X = df.drop("prix_DH", axis=1)
        y = df["prix_DH"]

        # Split data (same as training)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        print(f"✅ Train/Test split: {len(X_train)} / {len(X_test)} samples")

        # Load trained model
        model_path = "../models/xgboost_model.pkl"
        if not os.path.exists(model_path):
            print(f"❌ Model not found at {model_path}")
            return

        print(f"\n💾 Loading model from {model_path}...")
        model = joblib.load(model_path)
        print("✅ Model loaded successfully")

        # Check overfitting
        results = check_overfitting(model, X_train, y_train, X_test, y_test, "XGBoost")

        # Summary
        print("\n" + "="*70)
        print("📋 SUMMARY")
        print("="*70)
        print(f"\nModel Status: {results['severity']}")
        print(f"R² Gap: {results['r2_gap']:.4f}")
        print(f"\nRecommendation:")
        if results['severity'] == 'GOOD':
            print("✅ Model is well-tuned and ready for production!")
        elif results['severity'] == 'MILD':
            print("⚠️ Model is acceptable but could benefit from regularization")
        elif results['severity'] == 'MODERATE':
            print("⚠️ Model shows moderate overfitting - consider adding regularization")
        else:
            print("🚨 Model severely overfits - needs adjustments")
        
        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()