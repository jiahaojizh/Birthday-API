import sqlite3 as sql

DB_NAME = "../database/birthday.db"

def createDB():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE birthday(
        username TEXT PRIMARY KEY,
        birthday TEXT NOT NULL
        )""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()