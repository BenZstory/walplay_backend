from . import app, login_manager
from flask import Flask, request, jsonify, flash
from models import UserInfo, Role, init_db, db
from flask_sqlalchemy import SQLAlchemy
from flask import logging
from flask_login import login_user, login_required, LoginManager, flash, logout_user, make_secure_token, current_user
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import json


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


@login_manager.token_loader
def load_token(token):
    return UserInfo.query.filter(UserInfo.token == token)


@app.route('/register', methods=["POST"])
def register():
    try:
        jsonData = json.dumps(request.json)
        data = json.loads(jsonData)
        cell = data['cell']
        pwd = data['password']
        result = UserInfo.query.filter(UserInfo.cell == cell).first()
        if result is None:
            u = UserInfo(cell=cell, password=pwd)
            response = {"code": 0}
            token = u.get_auth_token()
            db.session.add(u)
            db.session.commit()
            return "token: "+token #TODO return code+token
        else:
            response = {"code": 1}
            return jsonify(response)
    except (KeyError, TypeError, ValueError):
        return "json error!"


@app.route('/login', methods=["GET", "POST"])
def login():
    try:
        jsonData = json.dumps(request.json)
        data = json.loads(jsonData)
        cell = data['cell']
        pwd = data['password']
        user = UserInfo.get_with_cell(cell=cell)
        login_user(user, remember=False)
        return "User: "+user.cell+"  successfully logged in"
    except (KeyError, TypeError, ValueError):
        return "json error!"


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return 'Logged out'


@app.route('/testLogin', methods=["GET", "POST"])
@login_required
def test_login():
    return current_user.cell


@app.route('/', methods=["POST", "GET"])
def home():
    return 'HI, test successful!'
