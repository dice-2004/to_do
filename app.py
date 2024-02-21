from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import write_log
import os
import func

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


DATABASE = "DB.db"
TXT_LOG = "history.log"
DBTABLE = "event_data"
PASSKEY = "Aaqaqaq20!"


func.create_event_data()


@app.route("/")
def home():
    return redirect(url_for("top"))


@app.route("/top")
def top():
    write_log.WriteLog("/top", "GET", "connect web site.")
    return render_template("top.html")


@app.route("/to_do")
def to_do():
    data = []
    data = func.receiveAllData_to_do()
    write_log.WriteLog("/to_do", "GET", "connect web site.")
    return render_template("/to_do.html", datas=data)


@app.route("/administrator_to_do")
def administrator_to_do():
    data = []
    data = func.receiveAllData_to_do()
    write_log.WriteLog("/administrator_to_do", "GET", "connect web site.")
    return render_template("administrator_to_do.html", datas=data)


@app.route("/form_to_do", methods=["GET", "POST"])
def form_to_do():
    if request.method == "POST":
        passkey = request.form["password"]
        if passkey == PASSKEY:
            event = request.form["event"]
            time = request.form["time"]
            time = func.conversionTime(time)
            func.writeData_to_do(event,time)
            write_log.WriteLog("/form_to_do", "POST", "add data success!")
            return redirect(url_for("administrator"))
        else:
            write_log.WriteLog("/form_to_do", "POST", "passkey error.")
            return render_template("form_to_do.html", passs=0)
    else:
        write_log.WriteLog("/form_to_do", "GET", "connect web site.")
        return render_template("form_to_do.html", passs=1)


@app.route("/<int:ID>/delete_to_do")
def deltete_to_do(ID):
    func.deleteData_to_do(ID)
    write_log.WriteLog(
        "/" + str(ID) + "/delete_to_do", "GET", "delete data success! ID = " + str(ID)
    )
    return redirect(url_for("administrator_to_do"))


@app.route("/<int:ID>/update_to_do", methods=["GET", "POST"])
def update_to_do(ID):
    if request.method == "POST":
        passkey = request.form["password"]
        if passkey == "Aaqaqaq20!":
            event = request.form["event"]
            time = request.form["time"]
            time = func.conversionTime(time)
            func.update_to_do(event,time,ID)
            write_log.WriteLog("/" + str(ID) + "/update_to_do","POST","update data success! ID = " + str(ID),)
            return redirect(url_for("administrator_to_do"))
        else:
            data=func.receiveData_to_do_ID(ID)
            write_log.WriteLog("/" + str(ID) + "/update_to_do","POST","passkey error. ID = " + str(ID),)
            return render_template("update_to_do.html", passs=0, datas=data)
    else:
        data=func.receiveData_to_do_ID(ID)
        write_log.WriteLog("/" + str(ID) + "/update_to_do", "GET", "connect web site. ID = " + str(ID))
        return render_template("update_to_do.html", passs=1, datas=data)


@app.route("/administrator")  # 管理者用ページ
def administrator():
    write_log.WriteLog("/administrator", "GET", "connect web site.")
    return render_template("administrator.html")


if __name__ == "__main__":  # Flask起動
    app.run(port=int("5000"), debug=True, host="localhost")
    # 開発時 -> port=int("5000"),debug=True,host='localhost'
    # 実装時 -> port=int("5000"),debug=True,host='localhost'
