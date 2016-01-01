from . import app, login_manager
from flask import Flask, request, jsonify, flash
from models import UserInfo, Role
from database import db_session, init_db
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask_login import login_user, login_required, LoginManager, flash, logout_user, make_secure_token
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import json


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(userid):
    return UserInfo.get(userid)

# @login_manager.request_loader
# def load_user_from_request(request):


@login_manager.token_loader
def load_token(token):
    print("get token")
    # user = UserInfo.get_with_token(token)
    # if not user:
    #     return None
    user = UserInfo()
    return user


@app.route('/register', methods=["POST"])
def register():
    '''
    try:
        jsonData = json.dumps(request.json)
        data = json.loads(jsonData)
        cell = data['cell']
        pwd = data['password']
        session = db_session()
        result = session.query(UserInfo).filter(UserInfo.cell == cell).first()
        if result is None:
            u = UserInfo(cell=cell, password=pwd)
            db_session.add(u)
            db_session.commit()
            response = '{"code":0}'
            token = u.generate_auth_token()
            return jsonify(token) #TODO return code+token
            # return "Successfully registered!"
        else:
            response = '{"code":1}'
            return jsonify(response)
            # return "User already exists"
    except (KeyError, TypeError, ValueError):
        return "json error!"
'''

    jsonData = json.dumps(request.json)
    data = json.loads(jsonData)
    cell = data['cell']
    pwd = data['password']
    session = db_session()
    result = session.query(UserInfo).filter(UserInfo.cell == cell).first()
    if result is None:
        u = UserInfo(cell=cell, password=pwd)
        db_session.add(u)
        db_session.commit()
        response = {"code": 0}
        token = u.generate_auth_token()
        return token #TODO return code+token
        # return "Successfully registered!"
    else:
        response = {"code": 1}
        return jsonify(response)
        # return "User already exists"


@app.route('/login', methods=["GET", "POST"])
def login():
    jsonData = json.dumps(request.json)
    data = json.loads(jsonData)
    cell = data['cell']
    pwd = data['password']
    user = UserInfo.get_with_cell(cell=cell)
    login_user(user, remember=True)
    return type(user)


@app.route('/testtoken', methods=["GET"])
@login_required
def testtoken():
    return "nice"


@app.route('/', methods=["POST", "GET"])
def home():
    return 'HI, test successful!'
