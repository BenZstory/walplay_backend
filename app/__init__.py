from flask import Flask
from models import UserInfo, Role
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)

from . import views