import datetime
import sqlite3


class db_worker:
    def __init__(self, path='DB/myDB.db'):
        super().__init__()
        self.conn = None
        self.cur = None
        self.connect(path)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def connect(self, path='DB/myDB.db'):
        try:
            self.conn = sqlite3.connect(path)
            self.cur = self.conn.cursor()
            print('Connected')
        except sqlite3.Error as error:
            print("Error while working with SQLite in <connect>", error)

    def check_login(self, login, password):
        try:
            self.cur.execute("SELECT fname, lname FROM employees WHERE login=? AND password=?", (login, password))
            self.conn.commit()
            ans = self.cur.fetchone()
            print('Data received')
            # print(ans)
            return ans
        except sqlite3.Error as error:
            print("Error while working with SQLite in <check_login>", error)

    def search(self, request):
        t = str(datetime.date(2005, 3, 14))
        return [('Петр', 'Исаев', t), ('Мария', 'Миронова', t)]

    def child_card(self, request):
        return (1, 'images/photo1.jpg', 'Петр', 'Исаев', datetime.date(2005, 3, 14), (('Мария', 'Ивановна', 'Исаева', '+79271804313, +72342356454', 'мама'),
                                                ('Игорь', 'Петрович', 'Иcаев', '+71234567283', 'папа')))

    def update(self, request):
        print('Saved:', request)

    def delete(self, request):
        print('Deleted: ', request)

