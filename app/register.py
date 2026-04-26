from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from auth import register_user


class RegisterPage(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()

        self.username = QLineEdit(); self.username.setPlaceholderText("Username")
        self.password = QLineEdit(); self.password.setPlaceholderText("Password")
        self.email = QLineEdit(); self.email.setPlaceholderText("Email")
        self.phone = QLineEdit(); self.phone.setPlaceholderText("+212 Phone")
        self.country = QLineEdit(); self.country.setPlaceholderText("Country")
        self.birth = QLineEdit(); self.birth.setPlaceholderText("Birthdate (YYYY-MM-DD)")

        self.msg = QLabel("")

        btn = QPushButton("Create Account")
        btn.clicked.connect(self.save)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.email)
        layout.addWidget(self.phone)
        layout.addWidget(self.country)
        layout.addWidget(self.birth)
        layout.addWidget(btn)
        layout.addWidget(self.msg)

        self.setLayout(layout)

    def save(self):
        register_user(
            self.username.text(),
            self.password.text(),
            self.email.text(),
            self.phone.text(),
            self.country.text(),
            self.birth.text()
        )

        self.msg.setText("Account Created ✅")
        self.controller.show_login()