from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import db
import write_log
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


DATABASE = "DB.db"
TXT_LOG = 'history.log'
DBTABLE=("event_data","user_data")




db.create_event_data()


@app.route("/")
def home():
    return redirect(url_for("top"))


@app.route("/top")
def top():
    write_log.WriteLog("/top","GET","connect web site.")
    return render_template("top.html")



@app.route("/to_do")
def to_do():
    write_log.WriteLog("/to_do","GET","connect web site.")
    con = sqlite3.connect(DATABASE)
    db_data = con.execute("SELECT * FROM event_data").fetchall()
    con.close()
    data = [{"event": row[0], "day": row[1]} for row in db_data]
    return render_template("/to_do.html", datas=data)


@app.route("/form_to_do", methods=["GET", "POST"])
def form_to_do():
    if request.method == "POST":
        passkey=request.form["password"]
        if passkey=="Aaqaqaq20!":
            event = request.form["event"]
            day = request.form["day"]
            print(day)
            year,month,day=day.split("-")
            day,time=day.split("T")
            day=year+"/"+month+"/"+day+" "+time
            con = sqlite3.connect(DATABASE)
            con.execute("INSERT INTO event_data VALUES (?, ?)", (event, day))
            con.commit()
            con.close()
            write_log.WriteLog("/form_to_do","POST","success!")
            return redirect(url_for("administrator"))
        else:
            write_log.WriteLog("/form_to_do","POST","passkey error.")
            return render_template("form_to_do.html", passs=0)
    else:
        write_log.WriteLog("/form_to_do","GET","connect web site.")
        return render_template("form_to_do.html", passs=1)



@app.route("/administrator")
def administrator():
    write_log.WriteLog("/administrator","GET","connect web site.")
    return render_template("administrator.html")


if __name__ == "__main__":  # Flask起動
    app.run(port=int("5000"), debug=True, host="localhost")
    # 開発時 -> port=int("5000"),debug=True,host='localhost'
    # 実装時 -> port=int("5000"),debug=True,host='localhost'
