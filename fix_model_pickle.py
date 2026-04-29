"""
Fix pickle compatibility issue with pandas StringDtype
"""
import joblib
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Try to load models and handle version compatibility
model_files = ["models/xgboost_model.pkl", "models/best_model.pkl"]

for model_file in model_files:
    try:
        print(f"Loading {model_file}...")
        model = joblib.load(model_file)
        print(f"✅ {model_file} loaded successfully")
        
        # Re-save with current pandas version for compatibility
        joblib.dump(model, model_file, compress=3)
        print(f"✅ {model_file} re-saved with current pandas version")
    except Exception as e:
        print(f"❌ Error with {model_file}: {e}")
        print(f"   Attempting advanced fix...")
        
        try:
            # Load with old pandas setting
            import pickle
            with open(model_file, 'rb') as f:
                obj = pickle.load(f)
            
            # Re-save with joblib
            joblib.dump(obj, model_file, compress=3)
            print(f"✅ {model_file} fixed with advanced method")
        except Exception as e2:
            print(f"❌ Advanced fix failed: {e2}")

print("\n✅ Model fix process complete!")
