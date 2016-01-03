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
        jsonData = json.dumps(request.json)
        data = json.loads(jsonData)
        cell = data['cell']
        pwd = data['password']
        result = UserInfo.query.filter(UserInfo.cell == cell).first()
        if result is None:
            u = UserInfo(cell=cell, password=pwd)
            response = {"code": 0}
            db.session.add(u)
            db.session.commit()
            token = u.get_auth_token()
            return "token: "+token #TODO return code+token
        else:
            response = {"code": 1}
            return jsonify(response)
    except (KeyError, TypeError, ValueError):
        return "json error!"


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'Authorization' in request.headers:
        user = UserInfo.get_with_token(request.headers['Authorization'])
        if user is not None:
            login_user(user)
            return "User: "+user.cell+"  successfully logged in by token"
    try:
        json_data = json.dumps(request.json)
        data = json.loads(json_data)
        cell = data['cell']
        pwd = data['password']
        user = UserInfo.get_with_cell(cell=cell)
        if (user is not None) and (user.password == pwd):
            login_user(user, remember=False)
            return "User: "+user.cell+"  successfully logged in by pwd"
        else:
            return 'Wrong username or pwd!'
    except (KeyError, TypeError, ValueError):
        return "json error!"


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return 'Logged out'


@appp.route("/add_spot", methods=["POST"])
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

        spot = SpotInfo(user_id=user_id, latitue=latitude, longitude=longitude,
                        radius=radius, time=create_time, title=title)

        db.session.add(spot)
        db.session.commit()

        return spot.__repr__()
    except (KeyError, TypeError, ValueError):
        return "json error!"


@app.route('/testLogin', methods=["GET", "POST"])
@login_required
def test_login():
    return current_user.id


@app.route('/', methods=["POST", "GET"])
def home():
    return 'HI, test successful!'
