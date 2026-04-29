"""
ui/splash_screen.py - Animated Splash Screen
"""

import os

from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QProgressBar,
    QVBoxLayout, QWidget, QGraphicsColorizeEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFontDatabase, QColor


class SplashScreen(QMainWindow):

    STEPS = [
        (10,  "صبر شوية... كنفيقو السيستيم "),
        (35,  "كنسخنو الموديل ..."),
        (60,  "كنرتبو الواجهة بحال الناس ..."),
        (85,  "كلشي تقريبا واجد ..."),
        (100, "يلا بينا! "),
    ]

    STEP_INTERVAL_MS = 1400

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DarPredict")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()

        self._step_index = 0

        self._build_ui()
        self._start_animation()

    # ─────────────────────────────────────────────
    def _build_ui(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 🎨 Load font Alice (optional)
        QFontDatabase.addApplicationFont(
            os.path.join(base_dir, "..", "assets", "fonts", "Alice.ttf")
        )
        font_family = "'Alice', 'Segoe UI', 'Arial'"

        # ── ROOT ─────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # ── BACKGROUND FULLSCREEN ─────────────
        bg_path = os.path.normpath(
            os.path.join(base_dir, "..", "assets", "splash_bg.png")
        )

        self.bg_label = QLabel(central)
        self.bg_label.setGeometry(self.rect())

        bg_pixmap = QPixmap(bg_path)
        self.bg_label.setPixmap(bg_pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        # ── OVERLAY ─────────────────────────────
        overlay = QWidget(central)
        overlay.setStyleSheet("""
            background-color: rgba(10, 30, 30, 135);
        """)

        layout = QVBoxLayout(overlay)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # ── LOGO PNG + COLOR CHANGE ─────────────
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent;")

        logo_path = os.path.normpath(
            os.path.join(base_dir, "..", "assets", "logo.png")
        )

        pixmap = QPixmap(logo_path)

        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                160, 160,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(pixmap)

            # 🎨 change color to #e8e8dc
            effect = QGraphicsColorizeEffect()
            effect.setColor(QColor("#e8e8dc"))
            effect.setStrength(1.0)
            icon_label.setGraphicsEffect(effect)

        else:
            icon_label.setText("LOGO")

        # ── TITLE ─────────────────────────────
        title = QLabel("DarPredict")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            color: #ffffff;
            font-family: {font_family};
            font-size: 54px;
            font-weight: bold;
            background: transparent;
            letter-spacing: 4px;
        """)

        # ── SUBTITLE ─────────────────────────────
        subtitle = QLabel("Merhba Bikom f DarPredict")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"""
            color: rgba(255, 255, 255, 200);
            font-family: {font_family};
            font-size: 22px;
            background: transparent;
        """)

        # ── PROGRESS BAR ─────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedSize(540, 16)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 45);
                border-radius: 8px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a3a3a,
                    stop:1 #2e9e88
                );
                border-radius: 8px;
            }
        """)

        # ── STATUS ─────────────────────────────
        self.status_label = QLabel("Démarrage...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"""
            color: rgba(255, 255, 255, 175);
            font-family: {font_family};
            font-size: 18px;
            background: transparent;
        """)

        # ── BUILD UI ─────────────────────────────
        layout.addStretch()
        layout.addWidget(icon_label)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(40)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addStretch()

        root_layout.addWidget(overlay)

    # ─────────────────────────────────────────────
    def resizeEvent(self, event):
        if hasattr(self, "bg_label"):
            self.bg_label.setGeometry(self.rect())
        super().resizeEvent(event)

    # ─────────────────────────────────────────────
    def _start_animation(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance_step)
        self._timer.start(self.STEP_INTERVAL_MS)

    def _advance_step(self):
        if self._step_index < len(self.STEPS):
            value, label = self.STEPS[self._step_index]
            self.progress_bar.setValue(value)
            self.status_label.setText(label)
            self._step_index += 1
        else:
            self._timer.stop()
            self._go_to_login()
            
            

    def _go_to_login(self):
        from ui.login_window import LoginWindow

        self._login = LoginWindow()

        # مهم: خليه مخفي أولاً
        self._login.setWindowOpacity(0.0)

        self._login.show()

        self.hide()

        from PyQt6.QtCore import QTimer, QPropertyAnimation

        def fade():
          self.anim = QPropertyAnimation(self._login, b"windowOpacity")
          self.anim.setDuration(200)
          self.anim.setStartValue(0.0)
          self.anim.setEndValue(1.0)
          self.anim.start()

          self.close()

        QTimer.singleShot(50, fade)
