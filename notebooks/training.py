"""
Model Training Script - Moroccan Housing Price Prediction
Trains and evaluates machine learning models on the cleaned housing dataset
"""

import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path

# Machine Learning Libraries
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Try to import XGBoost
try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

# Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

def load_data():
    """Load cleaned dataset"""
    print("\n" + "="*80)
    print("📂 LOADING DATA")
    print("="*80)
    
    data_path = "Data/processed/clean_house_prediction_dataset.csv"
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nDataset Preview:")
    print(df.head())
    
    return df

def prepare_features_target(df):
    """Prepare features and target variable"""
    print("\n" + "="*80)
    print("🔧 PREPARING FEATURES & TARGET")
    print("="*80)
    
    # Separate features and target
    X = df.drop("prix_DH", axis=1)
    y = df["prix_DH"]
    
    print(f"✅ Features: {X.shape[1]} columns")
    print(f"✅ Target: {y.shape[0]} samples")
    print(f"\nFeatures: {list(X.columns)}")
    print(f"Target variable: prix_DH")
    
    return X, y

def split_data(X, y):
    """Split data into train and test sets"""
    print("\n" + "="*80)
    print("✂️ SPLITTING DATA")
    print("="*80)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    print(f"✅ Training set: {X_train.shape[0]} samples ({(1-TEST_SIZE)*100:.0f}%)")
    print(f"✅ Test set: {X_test.shape[0]} samples ({TEST_SIZE*100:.0f}%)")
    
    return X_train, X_test, y_train, y_test

def create_preprocessing_pipeline(X):
    """Create preprocessing pipeline"""
    print("\n" + "="*80)
    print("🔄 CREATING PREPROCESSING PIPELINE")
    print("="*80)
    
    # Identify numeric and categorical features
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    
    print(f"✅ Numeric features: {len(numeric_features)}")
    print(f"✅ Categorical features: {len(categorical_features)}")
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('scaler', StandardScaler())
            ]), numeric_features),
            ('cat', Pipeline([
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ]), categorical_features) if categorical_features else None
        ]
    )
    
    # Remove None values
    preprocessor.transformers_ = [t for t in preprocessor.transformers if t is not None]
    preprocessor.transformers = [t for t in preprocessor.transformers if t is not None]
    
    print("✅ Preprocessing pipeline created")
    
    return preprocessor, numeric_features, categorical_features

def train_models(X_train, X_test, y_train, y_test, preprocessor, numeric_features, categorical_features):
    """Train multiple models"""
    print("\n" + "="*80)
    print("🤖 TRAINING MODELS")
    print("="*80)
    
    models = {}
    results = {}
    
    # Model 1: Linear Regression
    print("\n1️⃣ Training Linear Regression...")
    lr_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])
    lr_pipeline.fit(X_train, y_train)
    lr_pred = lr_pipeline.predict(X_test)
    lr_r2 = r2_score(y_test, lr_pred)
    lr_mae = mean_absolute_error(y_test, lr_pred)
    models['Linear Regression'] = lr_pipeline
    results['Linear Regression'] = {'R2': lr_r2, 'MAE': lr_mae}
    print(f"   ✅ R² Score: {lr_r2:.4f}")
    print(f"   ✅ MAE: ${lr_mae:,.2f}")
    
    # Model 2: Random Forest
    print("\n2️⃣ Training Random Forest...")
    rf_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1))
    ])
    rf_pipeline.fit(X_train, y_train)
    rf_pred = rf_pipeline.predict(X_test)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    models['Random Forest'] = rf_pipeline
    results['Random Forest'] = {'R2': rf_r2, 'MAE': rf_mae}
    print(f"   ✅ R² Score: {rf_r2:.4f}")
    print(f"   ✅ MAE: ${rf_mae:,.2f}")
    
    # Model 3: Gradient Boosting
    print("\n3️⃣ Training Gradient Boosting...")
    gb_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', GradientBoostingRegressor(n_estimators=100, random_state=RANDOM_STATE))
    ])
    gb_pipeline.fit(X_train, y_train)
    gb_pred = gb_pipeline.predict(X_test)
    gb_r2 = r2_score(y_test, gb_pred)
    gb_mae = mean_absolute_error(y_test, gb_pred)
    models['Gradient Boosting'] = gb_pipeline
    results['Gradient Boosting'] = {'R2': gb_r2, 'MAE': gb_mae}
    print(f"   ✅ R² Score: {gb_r2:.4f}")
    print(f"   ✅ MAE: ${gb_mae:,.2f}")
    
    # Model 4: XGBoost (if available)
    if XGBOOST_AVAILABLE:
        print("\n4️⃣ Training XGBoost...")
        xgb_pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', XGBRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1))
        ])
        xgb_pipeline.fit(X_train, y_train)
        xgb_pred = xgb_pipeline.predict(X_test)
        xgb_r2 = r2_score(y_test, xgb_pred)
        xgb_mae = mean_absolute_error(y_test, xgb_pred)
        models['XGBoost'] = xgb_pipeline
        results['XGBoost'] = {'R2': xgb_r2, 'MAE': xgb_mae}
        print(f"   ✅ R² Score: {xgb_r2:.4f}")
        print(f"   ✅ MAE: ${xgb_mae:,.2f}")
    else:
        print("\n4️⃣ XGBoost: Not available (install with: pip install xgboost)")
    
    return models, results

def select_best_model(models, results):
    """Select best model based on R² score"""
    print("\n" + "="*80)
    print("🏆 MODEL SELECTION")
    print("="*80)
    
    best_model_name = max(results, key=lambda x: results[x]['R2'])
    best_model = models[best_model_name]
    best_r2 = results[best_model_name]['R2']
    best_mae = results[best_model_name]['MAE']
    
    print(f"\n🥇 Best Model: {best_model_name}")
    print(f"   R² Score: {best_r2:.4f}")
    print(f"   MAE: ${best_mae:,.2f}")
    
    print("\n📊 Model Comparison:")
    print("-" * 50)
    for model_name, metrics in sorted(results.items(), key=lambda x: x[1]['R2'], reverse=True):
        print(f"  {model_name:<20} | R²: {metrics['R2']:.4f} | MAE: ${metrics['MAE']:>12,.2f}")
    
    return best_model_name, best_model

def save_model(best_model, best_model_name):
    """Save best model to disk"""
    print("\n" + "="*80)
    print("💾 SAVING MODEL")
    print("="*80)
    
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    model_path = f"models/{best_model_name.lower().replace(' ', '_')}_model.pkl"
    joblib.dump(best_model, model_path)
    
    print(f"✅ Model saved: {model_path}")
    print(f"   Model: {best_model_name}")
    
    return model_path

def main():
    """Main training pipeline"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "🏠 MOROCCAN HOUSING PRICE PREDICTION - MODEL TRAINING".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Load data
        df = load_data()
        
        # Prepare features and target
        X, y = prepare_features_target(df)
        
        # Split data
        X_train, X_test, y_train, y_test = split_data(X, y)
        
        # Create preprocessing pipeline
        preprocessor, numeric_features, categorical_features = create_preprocessing_pipeline(X)
        
        # Train models
        models, results = train_models(X_train, X_test, y_train, y_test, 
                                       preprocessor, numeric_features, categorical_features)
        
        # Select best model
        best_model_name, best_model = select_best_model(models, results)
        
        # Save model
        model_path = save_model(best_model, best_model_name)
        
        # Final summary
        print("\n" + "="*80)
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"\n📋 Summary:")
        print(f"  • Best Model: {best_model_name}")
        print(f"  • Model saved to: {model_path}")
        print(f"  • Ready for predictions!")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
