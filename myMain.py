import os
import sys
from shutil import copy2
from uuid import uuid4

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QObject, pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox,
                             QMainWindow, QTableWidgetItem, QFileDialog)

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
        self.setFixedSize(self.width(), self.height())
        header = self.search_tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.employee_name_label.setText(f'{employee[0]}\n{employee[1]}')

        self.search_btn.clicked.connect(self.search)
        self.exit_btn.clicked.connect(self.ext)
        self.add_new_btn.clicked.connect(self.new_child)
        self.search_tbl.doubleClicked.connect(self.more_data)

    def search(self):
        ans = DB.search(self.search_edit.text())
        self.search_tbl.setRowCount(len(ans))
        for i, row in enumerate(ans):
            for j, elem in enumerate(row):
                self.search_tbl.setItem(i, j, QTableWidgetItem(elem))

    def new_child(self):
        self.form = ChildCard(self)
        self.form.show()

    def more_data(self):
        row_number = self.search_tbl.selectionModel().selectedIndexes()[0].row()
        ans = DB.child_card((self.search_tbl.item(row_number, 0).text(),
                             self.search_tbl.item(row_number, 1).text(),
                             self.search_tbl.item(row_number, 2).text()))
        print(ans)
        self.form = ChildCard(self, ans)
        self.form.show()

    def ext(self):
        self.form = LoginForm()
        self.form.show()
        self.close()


class ChildCard(QWidget):
    def __init__(self,parent,  card=None):
        super(QWidget, self).__init__()
        uic.loadUi('forms/ChildCard.ui', self)
        self.setFixedSize(self.width(), self.height())
        self.image_path = None
        self.parent = parent
        self.parent_tbl.setColumnHidden(0, True)
        if card is not None:
            self.image_path = card[1]
            self.id_lbl.setText(str(card[0]))
            self.photo_lbl.setPixmap(QPixmap(card[1]))
            self.fName_edit.setText(card[2])
            self.sName_edit.setText(card[3])
            self.bd_edit.setDate(QDate(card[4]))
            self.parent_tbl.setRowCount(len(card[5]))
            self.parent_tbl.setColumnWidth(4, 110)
            header = self.parent_tbl.horizontalHeader()
            # header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header = self.parent_tbl.verticalHeader()
            for i, row in enumerate(card[5]):
                for j, elem in enumerate(row):
                    self.parent_tbl.setItem(i, j, QTableWidgetItem(str(elem)))
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        clickable(self.photo_lbl).connect(self.load_photo)
        self.add_parent_btn.clicked.connect(self.add_parent)
        self.del_parent_btn.clicked.connect(self.del_parent)
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.ext)
        self.del_btn.clicked.connect(self.delete)

    def add_parent(self):
        row_ind = self.parent_tbl.rowCount()
        self.parent_tbl.insertRow(row_ind)
        for col in range(self.parent_tbl.columnCount()):
            self.parent_tbl.setItem(row_ind, col, QTableWidgetItem(""))

    def del_parent(self):
        selected_rows = set()
        for elem in self.parent_tbl.selectedItems():
            selected_rows.add(elem.row())
        for row in sorted(selected_rows, reverse=True):
            self.parent_tbl.removeRow(row)

    def load_photo(self):
        img_dir = os.getcwd() + '/images/'
        self.image_path = QFileDialog.getOpenFileName(self, 'Open file', img_dir)[0]
        self.photo_lbl.setPixmap(QPixmap(self.image_path))
        print(self.image_path)

    def save(self):
        chk = True
        if self.fName_edit.text() == '' and self.sName_edit.text():
            chk = False
        parents_data = []
        for row in range(self.parent_tbl.rowCount()):
            parent = []
            for col in range(self.parent_tbl.columnCount()):
                parent.append(self.parent_tbl.takeItem(row, col).text())
            if parent.count('') != len(parent):
                parent[0] = parent[0]
                parents_data.append(tuple(parent))
        if len(parents_data) == 0:
            chk = False
        if chk:
            if self.image_path is not None:
                img_dir = os.getcwd() + '/images/'
                if img_dir not in self.image_path and 'images/' not in self.image_path:
                    # TODO: Resize image
                    new_fname = str(uuid4())
                    copy2(self.image_path, img_dir + new_fname)
                    self.image_path = new_fname
                else:
                    self.image_path = self.image_path.split('/')[-1]
                self.image_path = 'images/' + self.image_path

            data = (self.id_lbl.text(), self.image_path,
                    self.fName_edit.text(), self.sName_edit.text(), self.bd_edit.date().toPyDate(),
                    tuple(parents_data))
            DB.update(data)
            self.ext()
        else:
            msg = QMessageBox()
            msg.setText('Не все данные введены')
            msg.exec_()

    def ext(self):
        self.close()
        self.parent.search()

    def delete(self):
        if self.id_lbl.text() != '':
            qm = QMessageBox()
            ret = qm.question(self, '', "Вы хотите удалить карточку ученика?", qm.Yes | qm.No)
            if ret == qm.Yes:
                DB.delete(int(self.id_lbl.text()))
            else:
                return
        self.ext()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = LoginForm()
    form.show()

    sys.exit(app.exec_())
