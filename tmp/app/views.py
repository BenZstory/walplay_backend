from . import app

from flask import Flask,render_template,redirect,flash,request,session

from urllib2 import urlopen
from flask_login import LoginManager,login_required,login_url,login_user,logout_user



@app.route('/', methods=["POST","GET"])
def home():
    return 'HI, test successful!'







