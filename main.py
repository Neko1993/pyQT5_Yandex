import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *


def tableFill(self, res, headers):
    # задаем размер таблицы
    self.tableWidget.setColumnCount(len(headers))
    self.tableWidget.setRowCount(0)
    # создаем заголовки таблицы
    self.tableWidget.setHorizontalHeaderLabels(headers)
    # заполняем таблицу элементами
    for i, row in enumerate(res):
        self.tableWidget.setRowCount(
            self.tableWidget.rowCount() + 1)
        for j, elem in enumerate(row[1:]):
            self.tableWidget.setItem(
                i, j, QTableWidgetItem(str(elem)))


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('DB_UI.ui', self)
        self.connection = sqlite3.connect("bookvarenok.db")
        self.textEdit.setPlainText("SELECT * FROM child")
        self.select_data()
        # открываем окно поиска личной карточки ученика
        self.find_child.clicked.connect(self.child_request)

    def select_data(self):
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = self.textEdit.toPlainText()
        res = self.connection.cursor().execute(query).fetchall()
        headers = ['Имя', 'Фамилия', 'Дата рождения', 'Группа', 'Дата создания']
        # Заполняем таблицу элементами
        self.table = tableFill(self, res , headers)

    def initUI(self):
        # Зададим тип базы данных
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('bookvarenok.db')
        # И откроем подключение
        db.open()

        # QTableView - виджет для отображения данных из базы
        view = QTableView(self)
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('child')
        model.select()

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Пример работы с QtSql')

    def child_request(self):
        self.request = Request()
        self.request.show()


class Request(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('findChild.ui', self)
        self.connection = sqlite3.connect("bookvarenok.db")
        # self.select_data()
        self.search.clicked.connect(self.findChild)

    def findChild(self):
        self.name = self.child_name.text()
        self.surname = self.child_surname.text()
        query = f"SELECT * FROM child WHERE firstName = '{self.name}' and lastName = '{self.surname}'"
        res = self.connection.cursor().execute(query).fetchall()
        # определяем заголовки таблицы
        headers = ['Имя', 'Фамилия', 'Дата рождения', 'Группа', 'Дата создания']
        # Заполняем таблицу элементами
        self.table = tableFill(self, res, headers)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
