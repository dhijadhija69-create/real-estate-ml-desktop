import joblib
import os
import numpy as np

model_path = os.path.join(os.path.dirname(__file__), "../models/model.pkl")
model = joblib.load(model_path)

def predict_price(area, bedrooms, bathrooms):
    data = np.array([[area, bedrooms, bathrooms]])
    prediction = model.predict(data)
    return int(prediction[0])


# test
if __name__ == "__main__":
    print(predict_price(100, 2, 1))