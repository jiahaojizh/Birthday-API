import sqlite3 as sql

DB_NAME = "birthday.db"

def createDB():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE birthday(username, birthday)")
    conn.commit()
    conn.close()

def addValue():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    data = [
        ("jiahao", "1998-09-21"),
        ("diana", "1996-02-10"),
        ("cudi", "2021-09-25")
    ]
    cursor.executemany("""INSERT INTO birthday VALUES (?,?)""", data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()
    addValue()