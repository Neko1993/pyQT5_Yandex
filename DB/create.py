import sqlite3


def create_tables(conn):
    try:
        cur = conn.cursor()
        cur.execute("""DROP table IF EXIST employees;""")
        cur.execute("""DROP table IF EXIST children;""")
        conn.commit()
        print('Table\'s deleted')

        cur.execute("""CREATE TABLE employees(
                   employeeid INT PRIMARY KEY,
                   fname TEXT NOT NULL,
                   lname TEXT NOT NULL,
                   login TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL);
                """)
        conn.commit()

        cur.execute("""CREATE TABLE children(
                   childid INT PRIMARY KEY,
                   fname TEXT NOT NULL,
                   lname TEXT,
                   bd DATE);
                """)
        conn.commit()
        print('Table\'s created')
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        cur.close()


def add_data(conn):
    employees = [(1, 'Александр', 'Попов', 'admin', 'pass'),
             (2, 'Иван', 'Петров', 'user', '1')]
    try:
        cur = conn.cursor()
        cur.executemany("INSERT INTO employees VALUES(?, ?, ?, ?, ?);", employees)
        conn.commit()
        print('Employees added')
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
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
