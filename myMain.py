import datetime
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QObject, pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap, QPicture
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QMainWindow, QTableWidgetItem)

from DB.tools import db_worker

DB = db_worker()


def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('forms/LoginWidget.ui', self)
        self.setFixedSize(300, 200)
        self.login_btn.clicked.connect(self.check_password)

    def check_password(self):
        ans = DB.check_login(self.login_text.text(), self.password_text.text())

        if ans is not None:
            self.form = MainWindow(ans)
            self.form.show()
            self.close()
        else:
            msg = QMessageBox()
            msg.setText('Данные введены не верно')
            msg.exec_()


class MainWindow(QMainWindow):
    def __init__(self, employee):
        super(MainWindow, self).__init__()
        uic.loadUi('forms/MainWindow.ui', self)
        header = self.search_tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.employee_name_label.setText(f'{employee[0]}\n{employee[1]}')

        self.search_btn.clicked.connect(self.search)
        self.exit_btn.clicked.connect(self.ext)
        self.search_tbl.doubleClicked.connect(self.more_data)

    def search(self):
        ans = DB.search(self.search_edit.text())
        print(ans)
        self.search_tbl.setRowCount(len(ans))
        for i, row in enumerate(ans):
            for j, elem in enumerate(row):
                self.search_tbl.setItem(i, j, QTableWidgetItem(elem))
        print('done')

    def more_data(self):
        row_number = self.search_tbl.selectionModel().selectedIndexes()[0].row()
        ans = DB.child_card((self.search_tbl.item(row_number, 0).text(),
                             self.search_tbl.item(row_number, 1).text(),
                             self.search_tbl.item(row_number, 2).text()))
        print(ans)
        self.form = ChildCard(ans)
        self.form.show()

    def ext(self):
        self.form = LoginForm()
        self.form.show()
        self.close()


class ChildCard(QWidget):
    def __init__(self, card):
        super(QWidget, self).__init__()
        uic.loadUi('forms/ChildCard.ui', self)
        self.image_path = card[1]

        self.id_lbl.setText(str(card[0]))
        self.photo_lbl.setPixmap(QPixmap(card[1]))
        self.fName_edit.setText(card[2])
        self.sName_edit.setText(card[3])
        self.bd_edit.setDate(QDate(card[4]))
        self.parent_tbl.setRowCount(len(card[5]))
        self.parent_tbl.setColumnWidth(3, 110)
        header = self.parent_tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header = self.parent_tbl.verticalHeader()
        for i, row in enumerate(card[5]):
            for j, elem in enumerate(row):
                self.parent_tbl.setItem(i, j, QTableWidgetItem(elem))
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        # self.photo_lbl.doubleClicked.connect(self.load_photo)
        clickable(self.photo_lbl).connect(self.load_photo)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.ext)

    def load_photo(self):
        print('clicked')
        pass

    def save(self):
        parents_data = []
        for row in range(self.parent_tbl.rowCount()):
            parent = []
            for col in range(self.parent_tbl.columnCount()):
                parent.append(self.parent_tbl.takeItem(row, col).text())
            parents_data.append(tuple(parent))
        data = (
        self.id_lbl.text(), None, self.fName_edit.text(), self.sName_edit.text(), self.bd_edit.date().toPyDate(),
        tuple(parents_data))
        DB.update(data)
        self.close()

    def ext(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = MainWindow(('1', '2'))
    form.show()

    sys.exit(app.exec_())
