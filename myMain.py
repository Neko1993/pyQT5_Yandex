import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QMainWindow)

import DB.tools as DB


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('forms/LoginWidget.ui', self)
        self.setFixedSize(300, 200)
        self.login_btn.clicked.connect(self.check_password)

    def check_password(self):
        # conn = DB.connect()
        # DB.check_login(conn, self.login_text.text(), self.password_text.text())

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
