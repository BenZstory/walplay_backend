from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import query,session
from database import Base, db_session
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

secret_key = "BenZ_Key"

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class UserInfo(Base):
    __tablename__ = 'userInfo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(120))
    email = Column(String(120), unique=True)
    cell = Column(String(20))
    role_id = Column(Integer, ForeignKey('role.id')),

    def __init__(self, username=None, password=None, email=None, cell=None):
        self.username = username
        self.password = password
        self.email = email
        self.cell = cell

    def __repr__(self):
        return '&s (%r, %r)' % (self.__class__.__name__, self.name, self.email)

    def is_authenticated(self):
        return True

    def is_activate(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_auth_token(self):
        return self.cell   #TODO a better token

    def generate_auth_token(self, expiration=2592000):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def get_with_cell(cell):
        user = UserInfo.query.get(UserInfo.cell == cell)
        return user

    @staticmethod
    def get_with_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        q = session.query(UserInfo)
        user = UserInfo.query.get(data['id'])
        return user

    def get(self):
        return unicode(self.id)
'''
TokenList = (("1", "13122386668"),
             ("2", "13122386669")
             )
'''







