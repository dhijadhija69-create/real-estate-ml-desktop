"""
ui/signup_window.py - Registration Screen
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from auth.auth_manager import AuthManager


class WinBtn(QPushButton):
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"
    RESTORE  = "restore"
    CLOSE    = "close"

    def __init__(self, kind: str, parent=None):
        super().__init__(parent)
        self.kind = kind
        self.setFixedSize(46, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)

        if kind == self.CLOSE:
            self.setStyleSheet("""
                QPushButton { background: transparent; border: none; }
                QPushButton:hover { background: #c42b1c; }
                QPushButton:pressed { background: #9e2112; }
            """)
        else:
            self.setStyleSheet("""
                QPushButton { background: transparent; border: none; }
                QPushButton:hover { background: rgba(0,0,0,0.08); }
                QPushButton:pressed { background: rgba(0,0,0,0.15); }
            """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # rouge on close hover → white icon
        if self.kind == self.CLOSE and self.underMouse():
            color = QColor("#ffffff")
        else:
            color = QColor("#444444")

        pen = QPen(color, 1.2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        cx, cy = self.width() // 2, self.height() // 2
        s = 5

        if self.kind == self.MINIMIZE:
            painter.drawLine(cx - s, cy, cx + s, cy)

        elif self.kind == self.MAXIMIZE:
            painter.drawRect(cx - s, cy - s, s * 2, s * 2)

        elif self.kind == self.RESTORE:
            painter.drawRect(cx - s + 2, cy - s,     s * 2 - 2, s * 2 - 2)
            painter.drawRect(cx - s,     cy - s + 2, s * 2 - 2, s * 2 - 2)

        elif self.kind == self.CLOSE:
            painter.drawLine(cx - s, cy - s, cx + s, cy + s)
            painter.drawLine(cx + s, cy - s, cx - s, cy + s)

        painter.end()


class CustomTitleBar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self._parent   = parent
        self._drag_pos = QPoint()
        self.setFixedHeight(32)
        self.setObjectName("titleBar")
        self.setStyleSheet("""
            #titleBar { background: transparent; border: none; }
            #titleBarAppName { font-size: 12px; color: #333; font-weight: 500; }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 0, 0)
        layout.setSpacing(0)

        app_name = QLabel("🏠 DarPredict")
        app_name.setObjectName("titleBarAppName")
        layout.addWidget(app_name)
        layout.addStretch()

        self._btn_min   = WinBtn(WinBtn.MINIMIZE, self)
        self._btn_max   = WinBtn(WinBtn.MAXIMIZE, self)
        self._btn_close = WinBtn(WinBtn.CLOSE,    self)

        self._btn_min.clicked.connect(self._minimize)
        self._btn_max.clicked.connect(self._toggle_max)
        self._btn_close.clicked.connect(self._close)

        for btn in (self._btn_min, self._btn_max, self._btn_close):
            layout.addWidget(btn)

    def _update_max_icon(self):
        self._btn_max.kind = (
            WinBtn.RESTORE if self._parent.isMaximized() else WinBtn.MAXIMIZE
        )
        self._btn_max.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self._parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton and not self._drag_pos.isNull():
            self._parent.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = QPoint()

    def _minimize(self):  self._parent.showMinimized()
    def _close(self):     self._parent.close()
    def _toggle_max(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
        else:
            self._parent.showMaximized()
        self._update_max_icon()


class SignupWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.setWindowTitle("DarPredict — Créer un compte")

        # ✅ FramelessWindowHint QBAL show()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._build_ui()
        self.showFullScreen()

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("authBg")
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Title bar f-foq ──────────────────────────────────────────────────
        self.title_bar = CustomTitleBar(self)
        root_layout.addWidget(self.title_bar)

        # ── Card f-center ────────────────────────────────────────────────────
        outer = QWidget()
        outer.setObjectName("authBg")
        outer_layout = QVBoxLayout(outer)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setObjectName("authCard")
        card.setFixedWidth(400)
        layout = QVBoxLayout(card)
        layout.setSpacing(14)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Create Account")
        title.setObjectName("authTitle")
        sub = QLabel("Join us to predict your property value")
        sub.setObjectName("authSubtitle")

        name_lbl = QLabel("Full Name")
        name_lbl.setObjectName("fieldLabel")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Sara Lamlih")
        self.name_input.setObjectName("fieldInput")
        self.name_input.setFixedHeight(44)

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
        self.pw_input.returnPressed.connect(self._handle_signup)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        self.error_label.hide()

        btn_signup = QPushButton("Sign Up")
        btn_signup.setObjectName("btnSignup")
        btn_signup.setFixedHeight(48)
        btn_signup.clicked.connect(self._handle_signup)

        switch_row = QHBoxLayout()
        switch_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        have_account = QLabel("Already have an account?")
        have_account.setObjectName("switchText")
        login_link = QPushButton("Sign In")
        login_link.setObjectName("linkBtn")
        login_link.setCursor(Qt.CursorShape.PointingHandCursor)
        login_link.clicked.connect(self._go_to_login)
        switch_row.addWidget(have_account)
        switch_row.addWidget(login_link)

        layout.addWidget(title)
        layout.addWidget(sub)
        layout.addSpacing(10)
        layout.addWidget(name_lbl)
        layout.addWidget(self.name_input)
        layout.addWidget(email_lbl)
        layout.addWidget(self.email_input)
        layout.addWidget(pw_lbl)
        layout.addWidget(self.pw_input)
        layout.addWidget(self.error_label)
        layout.addSpacing(4)
        layout.addWidget(btn_signup)
        layout.addLayout(switch_row)

        outer_layout.addWidget(card)
        root_layout.addWidget(outer)



    # ── logic ─────────────────────────────────────────────────────────────────
    def _handle_signup(self):
        name     = self.name_input.text().strip()
        email    = self.email_input.text().strip()
        password = self.pw_input.text().strip()

        success, message = self.auth_manager.signup(name, email, password)
        if success:
            _, user = self.auth_manager.login(email, password)
            self._go_to_main(user)
        else:
            self.error_label.setText(message)
            self.error_label.show()

    def _go_to_login(self):
        from ui.login_window import LoginWindow
        self._login = LoginWindow()
        self._login.show()
        self.close()

    def _go_to_main(self, user):
        from ui.main_window import MainWindow
        self._main = MainWindow(user=user)
        self._main.show()
        self.close()