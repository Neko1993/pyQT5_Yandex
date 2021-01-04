import datetime
import sqlite3


def create_tables(conn):
    try:
        cur = conn.cursor()
        cur.execute("""DROP table employees;""")
        cur.execute("""DROP table children;""")
        cur.execute("""DROP table parents;""")
        conn.commit()
        print('Table\'s deleted')

        cur.execute("""CREATE TABLE employees(
                   employeeid INTEGER PRIMARY KEY AUTOINCREMENT,
                   fname TEXT NOT NULL,
                   lname TEXT NOT NULL,
                   login TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL);
                """)
        conn.commit()
        cur.execute("""CREATE TABLE children(
                   childid INTEGER PRIMARY KEY AUTOINCREMENT,
                   photo TEXT,
                   fname TEXT NOT NULL,
                   lname TEXT,
                   bd DATE);
                """)
        conn.commit()
        cur.execute("""CREATE TABLE parents(
                   parentid INTEGER PRIMARY KEY AUTOINCREMENT,
                   childid INT,
                   fname TEXT,
                   mname TEXT,
                   lname TEXT,
                   number TEXT,
                   role TEXT,
                   FOREIGN KEY (childid) REFERENCES children(childid));
                """)
        conn.commit()
        print('Table\'s created')
    except sqlite3.Error as error:
        print("Error while working with SQLite in <create_tables>", error)
    finally:
        cur.close()


def add_data(conn):
    employees = [
        (1, 'Александр', 'Попов', 'admin', 'pass'),
        (2, 'Иван', 'Петров', 'user', '1')
    ]
    children = [
        (1, None, 'Мария', 'Полшкова', datetime.date(2005, 3, 14)),
        (2, 'images/photo1.jpg', 'Игорь', 'Тулаев', datetime.date(2015, 5, 10)),
        (3, None, 'Михаил', 'Демьянов', datetime.date(2013, 7, 23)),
        (4, None, 'Михаил', 'Турышев', datetime.date(2014, 9, 21))
    ]
    parents = [
        (1, 1, 'Анна', 'Николаевна', 'Полшкова', '+79728676525', 'мама'),
        (2, 1, 'Петр', 'Филипович', 'Полшков', '+79728672525', 'папа'),
        (3, 2, 'Ольга', '', '', '+79628672525', 'бабушка'),
        (4, 3, 'Оксана', '', 'Демьянова', '+79608672525, +79208672525', 'мама'),
        (5, 4, 'Елена', '', '', '+79534572486', 'няня')
    ]
    try:
        cur = conn.cursor()
        cur.executemany("INSERT INTO employees VALUES(?, ?, ?, ?, ?);", employees)
        conn.commit()
        cur.executemany("INSERT INTO children VALUES(?, ?, ?, ?, ?);", children)
        conn.commit()
        cur.executemany("INSERT INTO parents VALUES(?, ?, ?, ?, ?, ?, ?);", parents)
        conn.commit()
        print('Data added')
    except sqlite3.Error as error:
        print("Error while working with SQLite in <add_data>", error)
    finally:
        cur.close()


def main():
    try:
        conn = sqlite3.connect('myDB.db')
        print('Connected')
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)

    create_tables(conn)
    add_data(conn)


if __name__ == '__main__':
    main()
