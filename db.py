import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('AA_db.sqlite')
    cur = conn.cursor()
    # cur.execute("CREATE TABLE applications (ID INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME DEFAULT CURRENT_TIMESTAMP, number INTEGER);")
    # conn.commit()
    

    # cur.execute('INSERT INTO applications (number) values (45)')
    # conn.commit()

    # cur.execute('SELECT * FROM applications')
    # data = cur.fetchall()
    # print(data)
    # cur.execute("delete from applications")
    # conn.commit()

    # cur.execute('SELECT * FROM applications')
    # data = cur.fetchall()
    # print(data)


    conn.close()
