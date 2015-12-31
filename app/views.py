from . import app, login_manager
from flask import Flask, request, jsonify, flash
from models import UserInfo, Role, TokenList
from database import db_session, init_db
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask_login import login_user, login_required, LoginManager, flash
import json


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader()
def load_user(userid):
    return UserInfo.get(UserInfo.id == userid)

@login_manager.request_loader
def load_user_from_request(request):

@login_manager.token_loader
def load_token(token):

@app.route('/register', methods=["POST"])
def register():
    jsonData = json.dumps(request.json)
    data = json.loads(jsonData)
    # try:
    cell = data['cell']
    pwd = data['password']
    session = db_session()
    result = session.query(UserInfo).filter(UserInfo.cell == cell).first()
    if result is None:
        u = UserInfo(cell=cell, password=pwd)
        db_session.add(u)
        db_session.commit()
        response = '{"code":0}'
        return jsonify(response)
        # return "Successfully registered!"
    else:
        response = '{"code":1}'
        return jsonify(response)
        # return "User already exists"

    # except (KeyError, TypeError, ValueError):
    #     return "json error!"

@app.route('/login', methods=['POST'])
def login():
    jsonData = json.dumps(request.json)
    data = json.loads(jsonData)
    login_user(user,True)

@app.route('/', methods=["POST", "GET"])
def home():
    return 'HI, test successful!'
