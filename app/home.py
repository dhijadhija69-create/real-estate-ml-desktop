from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class HomePage(QWidget):
    def __init__(self, controller):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("🏠 HOME PAGE")
        title.setStyleSheet("font-size: 24px;")

        btn = QPushButton("Go to Prediction")
        btn.clicked.connect(controller.show_predict)

        logout = QPushButton("Logout")
        logout.clicked.connect(controller.show_login)

        layout.addWidget(title)
        layout.addWidget(btn)
        layout.addWidget(logout)

        self.setLayout(layout)