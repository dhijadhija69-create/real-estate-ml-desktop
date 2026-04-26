import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget

from login import LoginPage
from home import HomePage
from predict import PredictPage


# 🎨 Theme
def set_dark_theme(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: white;
            font-size: 14px;
        }

        QPushButton {
            background-color: #2E86C1;
            padding: 8px;
            border-radius: 8px;
        }

        QPushButton:hover {
            background-color: #1B4F72;
        }

        QLineEdit {
            background-color: #1E1E1E;
            padding: 6px;
            border-radius: 6px;
            border: 1px solid #444;
        }
    """)


# 🧠 App class
class App(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login = LoginPage(self)
        self.home = HomePage(self)
        self.predict = PredictPage(self)

        self.addWidget(self.login)
        self.addWidget(self.home)
        self.addWidget(self.predict)

        self.setCurrentWidget(self.login)

        self.setWindowTitle("Real Estate ML App")
        self.resize(600, 400)

    def show_login(self):
        self.setCurrentWidget(self.login)

    def show_home(self):
        self.setCurrentWidget(self.home)

    def show_predict(self):
        self.setCurrentWidget(self.predict)


# 🚀 RUN APP
if __name__ == "__main__":
    app = QApplication(sys.argv)

    set_dark_theme(app)

    window = App()
    window.show()

    sys.exit(app.exec())