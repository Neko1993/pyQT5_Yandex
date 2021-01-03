import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QMainWindow)


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('LoginWidget.ui', self)
        self.setFixedSize(300, 200)

        self.login_btn.clicked.connect(self.check_password)

    def check_password(self):
        msg = QMessageBox()

        if self.login_text.text() == 'admin' and self.password_text.text() == 'pass':
            msg.setText('Успешно')
            msg.exec_()
        else:
            msg.setText('Данные введены не верно')
            msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())