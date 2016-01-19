from . import app, login_manager
from flask import Flask, request, jsonify
from models import UserInfo, db, SpotInfo, AudioInfo
from flask_login import login_user, login_required, logout_user, make_secure_token, current_user
# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import json
import time


@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


@login_manager.token_loader
def load_token(token):
    return UserInfo.query.filter(UserInfo.token == token)


@app.route('/register', methods=["POST"])
def register():
    try:
        cell = request.json['cell']
        pwd = request.json['password']
        result = UserInfo.query.filter(UserInfo.cell == cell).first()
        if result is None:
            u = UserInfo(cell=cell, password=pwd)
            token = u.get_auth_token()
            db.session.add(u)
            db.session.commit()
            response = {}
            response['code'] = 0
            response['token'] = token
            response['cell'] = cell
            return json.dumps(response)
            # return "token: "+token #TODO return code+token
        else:
            response = {}
            response['code'] = 1
            response['message'] = request
            return json.dumps(response)
    except (KeyError, TypeError, ValueError):
        response = {"code": -1}
        return json.dumps(response)


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'Authorization' in request.headers:
        user = UserInfo.get_with_token(request.headers['Authorization'])
        if user is not None:
            login_user(user)
            response = {}
            response['code'] = 0
            response['cell'] = user.cell
            response['token'] = user.token
            return json.dumps(response)
            # return "User: "+user.cell+"  successfully logged in by token"
    try:
        cell = request.json['cell']
        pwd = request.json['password']
        user = UserInfo.get_with_cell(cell=cell)
        if (user is not None) and (user.password == pwd):
            login_user(user, remember=True)
            response = {}
            response['code'] = 0
            response['cell'] = cell
            response['token'] = user.token
            return json.dumps(response)
        else:
            response = {'code': 1}
            return json.dumps(response)

    except (KeyError, TypeError, ValueError):
        response = {'code': -1}
        return json.dumps(response)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return 'Logged out'


@app.route("/add_spot", methods=["POST"])
@login_required
def add_spot():
    try:
        json_data = json.dumps(request.json)
        data = json.load(json_data)
        latitude = data['latitude']
        longitude = data['longitude']
        radius = data['radius']
        title = data['title']           #use user's preferences in the future
        create_time = data['time']
        if create_time is None:
            create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        user_id = current_user

        spot = SpotInfo(user_id=user_id, latitude=latitude, longitude=longitude,
                        radius=radius, time=create_time, title=title)

        db.session.add(spot)
        db.session.commit()

        return spot.__repr__()
    except (KeyError, TypeError, ValueError):
        return "json error!"


@app.route('/testLogin', methods=["GET", "POST"])
@login_required
def test_login():
    return current_user.__repr__()


@app.route('/', methods=["POST", "GET"])
def home():
    response = {}
    response['code'] = 0
    response['message'] = "Hi,test successful!"
    return json.dumps(response)
