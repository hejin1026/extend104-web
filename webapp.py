#!/usr/bin/env python
#coding: utf-8


from flask import Flask, request, redirect, render_template, url_for
from flask_login import current_user,LoginManager

import MySQLdb

app = Flask(__name__)
app.secret_key = '..... PUBLIC ....'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:public@192.168.1.111/extend104_new'

from db import db

from terminal.views import bp as term_bp
from user.views import bp as user_bp

from user.models import User

SAFE_ENDPOINTS = (None, 'static', 'user.login', 'user.logout', 'user.signup')


def config_login_mgr(app):
    login_mgr = LoginManager()
    login_mgr.login_view = 'user.login'
    login_mgr.login_message = u'请先登录系统.'
    
    @login_mgr.user_loader
    def load_user(id):
        return User.query.get(id)

    login_mgr.init_app(app)


@app.route('/')
def index():
    title = "test web"
    ''' 首页 '''
    return redirect(url_for('term.index'))
    
def config_sqlalchemy(app):
    db.init_app(app)
    db.app = app    

def register_blueprints(app):
    app.register_blueprint(term_bp)
    app.register_blueprint(user_bp)


def add_before(app):
    @app.before_request
    def before_request():
        if current_user.is_anonymous() and request.endpoint not in SAFE_ENDPOINTS:        
            print 'app.before_request: ', request.endpoint, current_user.is_authenticated(), current_user.is_anonymous()
            return redirect(url_for('user.login', next=request.url))
    

# ==============================================================================
#  Test running
# ==============================================================================    
if __name__ == '__main__':
    register_blueprints(app)
    config_login_mgr(app)
    add_before(app)
    config_sqlalchemy(app)
    app.run(host='0.0.0.0', port=8000, debug=True)
