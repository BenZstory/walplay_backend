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
    token = db.Column(db.String(255))
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
        db.session.commit()
        return t


# class MyReal(db.REAL):
#     scale = 10


class SpotInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)  #db.ForeignKey('user_info.id')
    resource_id = db.Column(db.Integer)  #db.ForeignKey('audio_info.id')
    create_time = db.Column(db.DateTime)
    latitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))
    radius = db.Column(db.String(20))
    spot_type = db.Column(db.Integer)
    next_point = db.Column(db.Integer)
    title = db.Column(db.String(120))

    def __init__(self, user_id, latitude, longitude, radius, resource=0, time=None,  spot_type=1, next_point=0, title=None):
        self.user_id = user_id
        self.resource = resource
        self.create_time = time
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.spot_type = spot_type
        self.next_point = next_point
        self.title = None

    def __repr__(self):
        return '<title %r>' % self.title


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer)
    resource_type = db.Column(db.Integer)   #db.ForeignKey('RType.id')
    detail_id = db.Column(db.Integer)

    def __init__(self, resource_id, detail_id, resource_type=1):
        self.resource_id = resource_id
        self.detail_id = detail_id
        self.resource_type = resource_type

    def __repr__(self):
        return '<source %r>' % self.resource_id


class AudioInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_dir = db.Column(db.String(255))

    def __init__(self, file_dir):
        self.file_dir = file_dir


def init_db():
    db.create_all()
    role = Role(1)
    db.session.add(role)
    db.session.commit()
