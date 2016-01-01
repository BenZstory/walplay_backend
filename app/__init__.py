from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:6668sql@localhost/walplay'
app.secret_key = 'TryToGuessMe'
app.config['SESSION_TYPE'] = 'filesystem'
track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

login_manager = LoginManager(app)
login_manager.login_view = '/login'
login_manager.session_protection = "strong"
login_manager.init_app(app)


from . import views