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
        sp = request.split()
        if len(sp) == 1:
            try:
                self.cur.execute("SELECT fname, lname, bd FROM children WHERE fname=? OR lname=?", (sp[0], sp[0]))
                self.conn.commit()
                ans = self.cur.fetchall()
                print('BACK: ', ans)
            except sqlite3.Error as error:
                print("Error while working with SQLite in <search>", error)
            return ans
        elif len(sp) == 2:
            try:
                self.cur.execute("SELECT fname, lname, bd FROM children WHERE (fname=? AND lname=?) OR (fname=? AND lname=?)", (sp[0], sp[1], sp[1], sp[0]))
                self.conn.commit()
                ans = self.cur.fetchall()
                print('BACK: ', ans)
            except sqlite3.Error as error:
                print("Error while working with SQLite in <search>", error)
            return ans
        return []

    def child_card(self, request):
        try:
            self.cur.execute("SELECT childid, photo,fname, lname, bd FROM children WHERE (fname=? AND lname=? AND bd=?)", request)
            self.conn.commit()
            ans = self.cur.fetchone()
        except sqlite3.Error as error:
            print("Error while working with SQLite in <child_card>", error)
        ans = list(ans)
        ans[4] = datetime.date.fromisoformat(ans[4])
        try:
            self.cur.execute("SELECT fname,mname, lname, number, role, parentid FROM parents WHERE childid=?", (str(ans[0])))
            self.conn.commit()
            parents = self.cur.fetchall()
        except sqlite3.Error as error:
            print("Error while working with SQLite in <child_card>", error)
        ans.append(parents)
        print('BACK: ', ans)
        return tuple(ans)


        return (1, 'images/photo1.jpg', 'Петр', 'Исаев', datetime.date(2005, 3, 14), (('Мария', 'Ивановна', 'Исаева', '+79271804313, +72342356454', 'мама'),
                                                ('Игорь', 'Петрович', 'Иcаев', '+71234567283', 'папа')))

    def update(self, request):
        print('Saved:', request)

    def delete(self, request):
        print('Deleted: ', request)

