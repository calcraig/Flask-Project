from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "abc123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))


def __init__(self, name, email):
    self.name = name
    self.email = email


@app.route("/")
def default():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        flash("Log in successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        else:
            return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    if "email" not in session:
        email = None
    else:
        email = session["email"]
    if "email_submit" in request.form:
        email = request.form["email"]
        session["email"] = email
    if "logout" in request.form:
        return redirect(url_for("logout"))
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user, email=email)
    else:
        flash("Log in required.", "info")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("Log out successful!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
