"""
ui/login_window.py - Login Screen
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt

# Import auth from the real project structure
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from auth.auth_manager import AuthManager

class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.setWindowTitle("DarPredict — Connexion")
        self.showFullScreen()  
        self._build_ui()

    def _build_ui(self):
        bg = QWidget()
        bg.setObjectName("authBg")
        self.setCentralWidget(bg)

        outer = QVBoxLayout(bg)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setObjectName("authCard")
        card.setFixedWidth(400)
        layout = QVBoxLayout(card)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Welcome Back to DarPredict")
        title.setObjectName("authTitle")
        sub = QLabel("Sign in to continue")
        sub.setObjectName("authSubtitle")

        email_lbl = QLabel("Email")
        email_lbl.setObjectName("fieldLabel")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("sara.lamlih@example.com")
        self.email_input.setObjectName("fieldInput")
        self.email_input.setFixedHeight(44)

        pw_lbl = QLabel("Password")
        pw_lbl.setObjectName("fieldLabel")
        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText("••••••••")
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_input.setObjectName("fieldInput")
        self.pw_input.setFixedHeight(44)
        self.pw_input.returnPressed.connect(self._handle_login)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        btn_login = QPushButton("Sign In")
        btn_login.setObjectName("btnPrimary")
        btn_login.setFixedHeight(48)
        btn_login.clicked.connect(self._handle_login)

        switch_row = QHBoxLayout()
        switch_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_account = QLabel("Don't have an account?")
        no_account.setObjectName("switchText")
        signup_link = QPushButton("Sign Up")
        signup_link.setObjectName("linkBtn")
        signup_link.setCursor(Qt.CursorShape.PointingHandCursor)
        signup_link.clicked.connect(self._go_to_signup)
        switch_row.addWidget(no_account)
        switch_row.addWidget(signup_link)

        layout.addWidget(title)
        layout.addWidget(sub)
        layout.addSpacing(10)
        layout.addWidget(email_lbl)
        layout.addWidget(self.email_input)
        layout.addWidget(pw_lbl)
        layout.addWidget(self.pw_input)
        layout.addWidget(self.error_label)
        layout.addSpacing(4)
        layout.addWidget(btn_login)
        layout.addLayout(switch_row)

        outer.addWidget(card)

    def _handle_login(self):
        email    = self.email_input.text().strip()
        password = self.pw_input.text().strip()

        if not email or not password:
            self._show_error("Veuillez remplir tous les champs.")
            return

        success, user = self.auth_manager.login(email, password)

        if success:
            self._go_to_main(user)
        else:
            self._show_error("Email ou mot de passe incorrect.")

    def _show_error(self, msg):
        self.error_label.setText(msg)
        self.error_label.show()

    def _go_to_signup(self):
        from ui.signup_window import SignupWindow
        self._signup = SignupWindow()
        self._signup.show()
        self.close()

    def _go_to_main(self, user):
        from ui.main_window import MainWindow
        self._main = MainWindow(user=user)
        self._main.show()
        self.close()