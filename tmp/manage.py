import sys
from flask import Flask
from flask.ext.script import Manager, Shell
from app import app


reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)


@manager.command
def hello():
    print 'hello'

if __name__ == '__main__':
    app.debug = True
    manager.run()
