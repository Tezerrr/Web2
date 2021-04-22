import datetime

import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from Settings import app, db


class Article(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    email = db.Column(db.String,
                      index=True, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime,
                             default=datetime.datetime.now)
    birth_day_date = db.Column(db.Integer, nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return '<Article %r>' % self.id
