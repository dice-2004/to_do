import sqlite3

DATABASE = "DB.db"

def create_event_data():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS event_data (ID INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT, day TEXT)")
    con.close()
