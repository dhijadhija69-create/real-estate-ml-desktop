import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from auth import register_user # تأكد بلي هاد الدالة كترجع True إلا نجح التسجيل و False إلا فشل

class RegisterPage(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        layout = QVBoxLayout()

        self.username = QLineEdit(); self.username.setPlaceholderText("Username")
        
        # 1. تصحيح الباسورد: باش يولي مخفي
        self.password = QLineEdit(); self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password) 

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
        # 2. التحقق من أن الخانات ماشي خاوية
        if not all([self.username.text(), self.password.text(), self.email.text()]):
            self.msg.setText("Please fill in all fields! ❌")
            self.msg.setStyleSheet("color: red;")
            return

        # 3. إرسال البيانات والتحقق من النتيجة
        try:
            # نفترض بلي register_user كترجع True إلا تم التسجيل
            success = register_user(
                self.username.text(),
                self.password.text(),
                self.email.text(),
                self.phone.text(),
                self.country.text(),
                self.birth.text()
            )

            if success:
                self.msg.setStyleSheet("color: green;")
                self.msg.setText("Account Created Successfully ✅")
                self.controller.show_login()
            else:
                self.msg.setStyleSheet("color: red;")
                self.msg.setText("Registration Failed! (Username/Email taken?)")
                
        except Exception as e:
            self.msg.setStyleSheet("color: red;")
            self.msg.setText(f"Error: {str(e)}")
            import sys
from PyQt6.QtWidgets import QApplication

# ... (l-class RegisterPage dyalek li k-t-b9a hna) ...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 3titha None 7it ma-3ndnich controller daba, 
    # ila kenti m-3refha f-controller khassk t-dkhlou hna
    window = RegisterPage(controller=None) 
    
    window.show()
    sys.exit(app.exec())