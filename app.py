from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3
import write_log
import os
import func

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

DATABASE = "DB.db"
TXT_LOG = "history.log"
DBTABLE = "event_data"

def login_required(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("login"))
        else:
            return func(*args, **kwargs)
    return wrapper


func.create_event_data()
func.create_user_data()
#func.add_user("dice","Aaqaqaq20!")

@app.route("/")
def home():
    return redirect(url_for("top"))

@app.route("/top")
def top():
    write_log.WriteLog("/top", "GET", "connect web site.")
    return render_template("top.html",key="login")


@app.route("/products")
def products():
    return render_template("products.html",key="login")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        PASS = func.receive_userdata(username)
        print(PASS)
        if PASS == password:
            session["username"] = username
            return redirect(url_for("administrator"))
        else:
            return render_template("login.html",error=2,key="login")
    else:
        return render_template("login.html",key="login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")




@app.route("/to_do")
def to_do():
    data = []
    data = func.receiveAllData_to_do()
    write_log.WriteLog("/to_do", "GET", "connect web site.")
    return render_template("/to_do.html", datas=data,key="login")


@app.route("/administrator_to_do")
@login_required
def administrator_to_do():
    data = []
    data = func.receiveAllData_to_do()
    write_log.WriteLog("/administrator_to_do", "GET", "connect web site.")
    return render_template("administrator_to_do.html", datas=data,key="logout")


@app.route("/form_to_do", methods=["GET", "POST"])
@login_required
def form_to_do():
    if request.method == "POST":
        event = request.form["event"]
        time = request.form["time"]
        time = func.conversionTime(time)
        func.writeData_to_do(event,time)
        write_log.WriteLog("/form_to_do", "POST", "add data success!")
        return redirect(url_for("administrator"))

    else:
        write_log.WriteLog("/form_to_do", "GET", "connect web site.")
        return render_template("form_to_do.html", passs=1,key="logout")


@app.route("/<int:ID>/delete_to_do")
@login_required
def deltete_to_do(ID):
    func.deleteData_to_do(ID)
    write_log.WriteLog(
        "/" + str(ID) + "/delete_to_do", "GET", "delete data success! ID = " + str(ID)
    )
    return redirect(url_for("administrator_to_do"))


@app.route("/<int:ID>/update_to_do", methods=["GET", "POST"])
@login_required
def update_to_do(ID):
    if request.method == "POST":

        event = request.form["event"]
        time = request.form["time"]
        time = func.conversionTime(time)
        func.update_to_do(event,time,ID)
        write_log.WriteLog("/" + str(ID) + "/update_to_do","POST","update data success! ID = " + str(ID),)
        return redirect(url_for("administrator_to_do"))

    else:
        data=func.receiveData_to_do_ID(ID)
        write_log.WriteLog("/" + str(ID) + "/update_to_do", "GET", "connect web site. ID = " + str(ID))
        return render_template("update_to_do.html", passs=1, datas=data,key="logout")


@app.route("/administrator")  # 管理者用ページ
@login_required
def administrator():
    write_log.WriteLog("/administrator", "GET", "connect web site.")
    return render_template("administrator.html",key="logout")


if __name__ == "__main__":  # Flask起動
    app.run(port=int("5000"), debug=True, host="localhost")
    # 開発時 -> port=int("5000"),debug=True,host='localhost'
    # 実装時 -> port=int("5000"),debug=True,host='localhost'
