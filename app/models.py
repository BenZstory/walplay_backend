from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


db = SQLAlchemy(app)
my_secret_key = "BenZ_Key"


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, role_id, name="default", description=None):
        self.role_id = role_id
        self.name = name
        self.description = description


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cell = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    token = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    def __init__(self, cell, password, email=None, role_id=1, username=None, token=None):
        self.cell = cell
        self.password = password
        self.email = email
        self.role_id = role_id
        self.username = username
        self.token = token

    def __repr__(self):
        return '<User %r>' % self.cell

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def get_with_cell(cell):
        user = UserInfo.query.filter(UserInfo.cell == cell).first()
        return user

    @staticmethod
    def get_with_id(user_id):
        user = UserInfo.query.get(UserInfo.id == user_id).first()
        return user

    @staticmethod
    def get_with_token(token):
        s = Serializer(secret_key=my_secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = UserInfo.query.get(data['id'])
        return user

    def get_auth_token(self, expiration=2592000):
        '''
        return a token encryped with id
        :return:
        '''
        s = Serializer(secret_key=my_secret_key, expires_in=expiration)
        t = s.dumps({'id': self.id})
        self.token = t
        return t


def init_db():
    db.create_all()
    role = Role(1)
    db.session.add(role)
    db.session.commit()

