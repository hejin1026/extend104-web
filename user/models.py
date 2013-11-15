#!/usr/bin/env python
#coding: utf-8

import hashlib

from flask_login import UserMixin

from db import db

from datetime import datetime


class User(db.Model, UserMixin):
    id          =   db.Column(db.Integer, primary_key=True)
    login       =   db.Column(db.String(16), nullable=False)
    password    =   db.Column(db.String(80), nullable=False)
    nick        =   db.Column(db.String(64))
    email       =   db.Column(db.String(32))
    created_at  =   db.Column(db.DateTime, default=datetime.now)
    updated_at  =   db.Column(db.DateTime)
    
    def check_passwd(self, passwd):
        print 'self.password:', self.password, passwd
        return self.password == User.crypted_password(passwd)            

    @staticmethod
    def crypted_password(passwd):
        return hashlib.sha256(passwd).hexdigest()
        
    @staticmethod
    def authenticate(username, passwd):
        user = User.query.filter(db.or_(User.login == username,
                                         User.email == username)).first()
        authenticated = user.check_passwd(passwd) if user else False
        print 'authenticate().user', user, passwd
        return user, authenticated
    
    @staticmethod
    def check_username(username):
        user = User.query.filter(User.login == username).first()
        return True if user else False