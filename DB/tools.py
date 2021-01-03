import sqlite3


def connect(path='DB/myDB.db'):
    try:
        conn = sqlite3.connect(path)
        print('Connected')
        return conn
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)


def check_login(conn, login, password):
    try:
        cur = conn.cursor()
        cur.execute("SELECT fname, lname FROM employees WHERE login=? AND password=?", (login, password))
        conn.commit()
        ans = cur.fetchone()
        print('Data received')
        print(ans)
        return ans
    except sqlite3.Error as error:
        print("Error while working with SQLite in <check_login>", error)
    finally:
        cur.close()
