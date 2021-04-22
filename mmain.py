import datetime

import sqlalchemy
from flask import Flask, render_template, redirect, request, flash
from data import db_session
from data.news import News
from werkzeug.security import generate_password_hash, check_password_hash
import random
from UserLogin import UserLogin
from forms.login import LoginForm
import requests
from FDataBase import FDataBase
from static.img.saved import save
from data.users import User
from forms.user import RegisterForm
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from keu import data_check
from data.Article import Article
from Settings import app, db




login_manager = LoginManager(app)
menu = ["Главная страница", "Сообщения", "Авторизация"]


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news, menu=menu)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if request.method == "POST":
        d, m, y = request.form["day"], request.form["month"], request.form["year"]
        if not data_check(d, m, y):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Не правильная дата рождения")
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            birth_day_date=f"{d}.{m}.{y}"
        )
        save(form.name.data, form.email.data, form.password.data, "reg")
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

def check_z(z):

    return f"Рак - {random.randint(50, 101)}%"

@app.route('/users')
def users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).desc()
    zz = []
    for u in users:
        z = u.birth_day_date
        zz.append(check_z(z))

    return render_template("users.html", title="Лента", users=users, zz=zz)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user)
        if user != None:
            if User.check_password(user, form.password.data):
                save(form.email.data, form.password.data, "log")
                return redirect("/")
            else:
                return render_template("login.html", title="Авторизация", menu=menu, form=form,
                                       message="Неверный email или пароль")
        else:
            return render_template("login.html", title="Авторизация", menu=menu, form=form,
                                   message="Неверный email")


    return render_template("login.html", title="Авторизация", menu=menu, form=form)

@app.route("/users/<int:id>")
def user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    zz = []
    zz.append(check_z(user.birth_day_date))
    return render_template("us_detail.html", us=user, zz=zz, title=user.name)

def main():
    db_session.global_init("db/blogs.db")
    app.run()
    # user = User()
    # user.name = "Пользователь 3454"
    # user.about = "биография пользователя 1"
    # user.email = "ema1il@email.ru"
    # user.birth_day_date = "8.7.2004"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()


if __name__ == '__main__':
    main()
