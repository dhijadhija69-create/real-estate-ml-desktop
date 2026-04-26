from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(BASE_DIR, "models", "model.pkl")

model = joblib.load(model_path)

# load ML model
#model = joblib.load("models/model.pkl")
model = joblib.load("../models/model.pkl")


class PredictPage(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()

        title = QLabel("💰 House Price Prediction")
        title.setStyleSheet("font-size: 22px;")

        # inputs
        self.area = QLineEdit()
        self.area.setPlaceholderText("Area (m²)")

        self.bedrooms = QLineEdit()
        self.bedrooms.setPlaceholderText("Bedrooms")

        self.bathrooms = QLineEdit()
        self.bathrooms.setPlaceholderText("Bathrooms")

        # result
        self.result = QLabel("")

        # buttons
        self.btn_predict = QPushButton("Predict")
        self.btn_predict.clicked.connect(self.predict)

        self.btn_back = QPushButton("Back to Home")
        self.btn_back.clicked.connect(controller.show_home)

        # layout
        layout.addWidget(title)
        layout.addWidget(self.area)
        layout.addWidget(self.bedrooms)
        layout.addWidget(self.bathrooms)
        layout.addWidget(self.btn_predict)
        layout.addWidget(self.result)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def predict(self):
        try:
            area = float(self.area.text())
            bedrooms = int(self.bedrooms.text())
            bathrooms = int(self.bathrooms.text())

            # validation
            if area <= 0 or bedrooms <= 0 or bathrooms <= 0:
                self.result.setText("❌ Values must be positive")
                return

            data = np.array([[area, bedrooms, bathrooms]])
            price = model.predict(data)[0]

            self.result.setText(f"💰 Predicted Price: {price:.2f}")

        except ValueError:
            self.result.setText("❌ Please enter valid numbers")
        except Exception as e:
            self.result.setText(f"❌ Error: {str(e)}")