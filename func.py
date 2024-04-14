import sqlite3
from flask import session,redirect,url_for

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

def create_user_data():
    con = sqlite3.connect(DATABASE)
    data=con.execute(
        "CREATE TABLE IF NOT EXISTS user_data (ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"
    ).fetchall()
    con.close()

    return data



def receiveAllData_to_do():
    con = sqlite3.connect(DATABASE)
    db_data = con.execute("SELECT * FROM event_data").fetchall()
    con.close()
    data = [{"ID": row[0], "event": row[1], "time": row[2]} for row in db_data]
    return data

def receive_userdata(username):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_data WHERE username = ?", (username,))
    db_data = cur.fetchone()
    con.close()
    if db_data:
        return db_data[2]  # パスワードを返す
    else:
        return None  # ユーザーデータが見つからない場合はNoneを返す

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


def add_user(username, password):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    # ユーザー名がすでに存在するかどうかをチェック
    cur.execute("SELECT * FROM user_data WHERE username = ?", (username,))
    existing_user = cur.fetchone()
    if existing_user:
        print("ユーザー名はすでに存在します。別のユーザー名を選択してください。")
        return

    # 新しいユーザーを挿入
    cur.execute("INSERT INTO user_data (username, password) VALUES (?, ?)", (username, password))
    con.commit()
    con.close()
