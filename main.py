"""
main.py - Point d'entrée de l'application
"""

import sys
import os

from PyQt6.QtWidgets import QApplication
from ui.splash_screen import SplashScreen


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DarPredict")

    # ── Load stylesheet safely ──
    qss_path = os.path.join(os.path.dirname(__file__), "ui", "style.qss")

    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    # ── Splash start ──
    splash = SplashScreen()
    splash.show()

    # prevent GC flicker
    sys._splash = splash

    sys.exit(app.exec())




if __name__ == "__main__":
    main()
