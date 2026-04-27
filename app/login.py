from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import csv


class LoginPage(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")

        self.msg = QLabel("")

        btn = QPushButton("Login")
        btn.clicked.connect(self.check)

        layout.addWidget(self.user)
        layout.addWidget(self.pwd)
        layout.addWidget(btn)
        layout.addWidget(self.msg)

        self.setLayout(layout)

    def check(self):
        username = self.user.text()
        password = self.pwd.text()

        try:
            with open("users.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)

                for row in reader:
                    if row[0] == username and row[1] == password:
                        self.controller.show_home()
                        return

            self.msg.setText("Wrong ❌")

        except BaseException:
            self.msg.setText("No users ❌")
