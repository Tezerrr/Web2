import sqlite3

from Settings import login_manager
from data import db_session
from data.users import User


class UserLogin:
    def fromDB(self, user_id, db_s):
        self.__user = db_s.query(User).filter(User.id == user_id).first()
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return UserLogin().fromDB(user_id, db_sess)


def getUser(user_id):
    try:
        db_sess = db_session.create_session()
        res = db_sess.query(User).filter(User.id == user_id).first()
        if not res:
            print(f"Пользователь {user_id} не найден")
        return False
    except sqlite3.Error as e:
        print(f"Ошибка получения данных из бд {e}")
    return False
