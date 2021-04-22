import datetime
import os

import sqlalchemy
from flask import Flask, render_template, redirect, request, flash, url_for
from data import db_session
from data.news import News
from werkzeug.security import generate_password_hash, check_password_hash
import random
from sovm import check_z, sov
from forms.login import LoginForm
import requests
from FDataBase import FDataBase
from static.img.saved import save
from data.users import User
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from keu import data_check
from data.Article import Article
from Settings import *
from forms.load_user import load_user

menu = ["Главная страница", "Сообщения", "Авторизация"]


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news, menu=menu)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    years = range(2006, 1900, -1)
    days = range(31, 0, -1)
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
    return render_template('register.html', title='Регистрация', form=form, years=years, days=days)


@app.route("/profile")
@login_required
def profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
    print(current_user.is_authenticated())
    return render_template("profile.html", u=user, current_user=current_user)

@app.route('/users')
@login_required
def users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    zz = []
    user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
    for u in users:
        z = u.birth_day_date
        zz.append(f"{check_z(z)}, Ваша совместимость -  {sov(check_z(z), user.birth_day_date)}%")

    return render_template("users.html", title="Лента", users=users, zz=zz)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login, password = form.email, form.password

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user != None:
            if User.check_password(user, form.password.data):
                save(form.email.data, form.password.data, "log")
                login_user(user)
                return redirect("profile")
            else:
                return render_template("login.html", title="Авторизация", menu=menu, form=form,
                                       message="Неверный email или пароль")
        else:
            return render_template("login.html", title="Авторизация", menu=menu, form=form,
                                   message="Неверный email")

    return render_template("login.html", title="Авторизация", menu=menu, form=form)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for("login") + '?next' + request.url)
    return response


@app.route("/users/<int:id>")
@login_required
def user(id):
    db_sess = db_session.create_session()
    z_user = db_sess.query(User).filter(User.id == id).first()
    zz = []
    user = db_sess.query(User).filter(User.id == current_user.get_id()).first()
    zz.append(f"{check_z(z_user.birth_day_date)}, Ваша совместимость -  {sov(check_z(z_user.birth_day_date), user.birth_day_date)}%")
    return render_template("us_detail.html", us=user, zz=zz, title=user.name)


@app.route("/message")
@login_required
def messages():
    return render_template("message.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/login")


def main():
    db_session.global_init("db/blogs.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



if __name__ == '__main__':
    main()
