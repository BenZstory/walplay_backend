from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base, db_session
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


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
        s = Serializer(app.config['BenZ_Key'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def get_with_token(token):
        s = Serializer(app.config['BenZ_Key'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = UserInfo.query.get(data['id'])
        return user

TokenList = (("1", "13122386668"),
             ("2", "13122386669")
             )








