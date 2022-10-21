import json
from datetime import datetime
from flask import Flask, render_template, session, redirect
from flask_bs4 import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length
app.config['SECRET_KEY'] = "sfjhbhndf/mnbh m,knbvfghhm,ggbm"
date = datetime.now()

class UserName(FlaskForm):
    userName = StringField("podaj swoje imię: ", validators=[DataRequired()])
    submit = SubmitField("Wyślij")

class LoginForm(FlaskForm):
    userLogin =StringField("Nazwa użytkownika:", validators=[DataRequired()])
    userPass = PasswordField("hasło", validators=[DataRequired(), Length(min=8, max=8)])
    submit =   SubmitField("Zaloguj")

users = {'userName':'admin', 'password':'password'}

@app.route('/')
def index():
    UserForm = UserName()
    return render_template('index.html', title="title", UserForm=UserForm)

@app.route('/dashboard', methods=["POST","GET"])
def dashboard():
    with open("data/grades.json") as gradesFile:
        grades = json.load(gradesFile)


    return render_template('dashboard.html', title="Dashboard",userLogin=session.get('userLogin'),date=date, grades=grades)

@app.route('/logIn', methods=["POST","GET"])
def logIn():
    login = LoginForm()
    if login.validate_on_submit():
        userLogin = login.userLogin.data
        userPass = login.userPass.data
        if userLogin == users["userName"] and userPass == users["password"]:

            session["userLogin"] = userLogin
            return redirect("/dashboard")
    return render_template('login.html', title="Logowanie", login=login, userLogin=session.get('userLogin'))

@app.route("/logOut")
def logOut():
    session.pop('userLogin')
    return redirect('logIn')

#
# @app.errorhandler(404)
# def pageNotFound(error):
#     return render_template("404.html"), 404
#
# @app.errorhandler(500)
# def internalServerError(error):
#     return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)