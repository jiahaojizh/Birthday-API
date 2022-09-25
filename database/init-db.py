import sqlite3 as sql

DB_NAME = "birthday.db"

def createDB():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE birthday(username, birthday)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB()