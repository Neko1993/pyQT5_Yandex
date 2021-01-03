import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QMainWindow)

from DB.tools import db_worker


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('forms/LoginWidget.ui', self)
        self.setFixedSize(300, 200)
        self.login_btn.clicked.connect(self.check_password)

    def check_password(self):
        DB = db_worker()
        ans = DB.check_login(self.login_text.text(), self.password_text.text())

        msg = QMessageBox()

        if ans is not None:
            self.form = MainWindow(ans)
            self.form.show()
            self.close()
            # msg.setText('Добро пожаловать,  '+ans[0]+'!')
            # msg.exec_()

        else:
            msg.setText('Данные введены не верно')
            msg.exec_()


class MainWindow(QMainWindow):
    def __init__(self, employee):
        super(MainWindow, self).__init__()
        uic.loadUi('forms/MainWindow.ui', self)
        self.employee_name_label.setText(f'{employee[0]}\n{employee[1]}')
        self.exit_btn.clicked.connect(self.ext)

    def ext(self):
        self.form = LoginForm()
        self.form.show()
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())
