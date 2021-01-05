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
                self.cur.execute(
                    "SELECT fname, lname, bd FROM children WHERE (fname=? AND lname=?) OR (fname=? AND lname=?)",
                    (sp[0], sp[1], sp[1], sp[0]))
                self.conn.commit()
                ans = self.cur.fetchall()
                print('BACK: ', ans)
            except sqlite3.Error as error:
                print("Error while working with SQLite in <search>", error)
            return ans
        return []

    def child_card(self, request):
        try:
            self.cur.execute(
                "SELECT childid, photo,fname, lname, bd FROM children WHERE (fname=? AND lname=? AND bd=?)", request)
            self.conn.commit()
            ans = self.cur.fetchone()
        except sqlite3.Error as error:
            print("Error while working with SQLite in <child_card>", error)
        ans = list(ans)
        ans[4] = datetime.date.fromisoformat(ans[4])
        try:
            self.cur.execute("SELECT parentid, fname,mname, lname, number, role FROM parents WHERE childid=?",
                             (str(ans[0])))
            self.conn.commit()
            parents = self.cur.fetchall()
        except sqlite3.Error as error:
            print("Error while working with SQLite in <child_card>", error)
        ans.append(parents)
        print('BACK: ', ans)
        return tuple(ans)

    def update(self, request):
        if request[0] == '':
            try:
                self.cur.execute("INSERT INTO children(photo, fname, lname,bd) VALUES(?,?,?,?)", request[1:5])
                self.conn.commit()
                new_id = self.cur.lastrowid
                self.cur.executemany(
                    "INSERT INTO parents(childid, fname, mname, lname, number, role) VALUES(?,?,?,?,?,?)",
                    [(new_id,) + tuple(request[5][i][1:]) for i in range(len(request[5]))])
                self.conn.commit()
                print('Created new child card')
            except sqlite3.Error as error:
                print("Error while working with SQLite in <update>", error)
        else:
            try:
                self.cur.execute("UPDATE children SET photo=?, fname=?, lname=?, bd=? where childid=?",
                                 tuple(request[1:5]) + (request[0],))
                self.conn.commit()
                for parent in request[5]:
                    if parent[0] == '':
                        self.cur.execute(
                            "INSERT INTO parents(childid, fname, mname, lname, number, role) VALUES(?,?,?,?,?,?)",
                            (request[0],) + parent[1:])
                    else:
                        data = (request[0],) + tuple(parent[1:]) + (parent[0],)
                        print('BACK try:', data)
                        self.cur.execute(
                            "UPDATE parents SET childid=?, fname=?, mname=?, lname=?, number=?, role=? where parentid=?",
                            tuple(data))
                    self.conn.commit()
                print('Updated child card')
            except sqlite3.Error as error:
                print("Error while working with SQLite in <update>", error)

    def delete(self, request):
        try:
            self.cur.execute("DELETE FROM parents WHERE childid=?", (str(request),))
            self.conn.commit()
            self.cur.execute("DELETE FROM children WHERE childid=?", (str(request),))
            self.conn.commit()
            print('Deleted: ', request)
        except sqlite3.Error as error:
            print("Error while working with SQLite in <child_card>", error)
