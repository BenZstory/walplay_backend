from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))


engine = create_engine('mysql+mysqlconnector://root:6668sql@localhost/testDB')

DBSession = sessionmaker(bind=engine)

session = DBSession()

new_user = User(id=5, name='Bob')

session.add(new_user)

session.commit()

session.close()