import sqlite3

DATABASE = "DB.db"


def conversionTime(day):
    year, month, day = day.split("-")
    day, time = day.split("T")
    time = year + "/" + month + "/" + day + " " + time
    return time


def create_event_data():
    con = sqlite3.connect(DATABASE)
    con.execute(
        "CREATE TABLE IF NOT EXISTS event_data (ID INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT, time TEXT)"
    )
    con.close()


def receiveAllData_to_do():
    con = sqlite3.connect(DATABASE)
    db_data = con.execute("SELECT * FROM event_data").fetchall()
    con.close()
    data = [{"ID": row[0], "event": row[1], "time": row[2]} for row in db_data]
    return data


def writeData_to_do(event,time):
    con = sqlite3.connect(DATABASE)
    con.execute("INSERT INTO event_data (event, time) VALUES (?, ?)", (event, time))
    con.commit()
    con.close()


def deleteData_to_do(ID):
    con = sqlite3.connect(DATABASE)
    con.execute("DELETE FROM event_data WHERE ID = ?", (ID,))
    con.commit()
    con.close()


def update_to_do(event,time,ID):
    con = sqlite3.connect(DATABASE)
    con.execute("UPDATE event_data SET event = ?, time = ? WHERE ID = ?",(event, time, ID),)
    con.commit()
    con.close()


def receiveData_to_do_ID(ID):
    con = sqlite3.connect(DATABASE)
    db_data = con.execute("SELECT * FROM event_data where ID = ?", (ID,)).fetchall()
    con.close()
    data = {"ID": db_data[0][0], "event": db_data[0][1], "time": db_data[0][2]}
    return data
