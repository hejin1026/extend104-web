#!/usr/bin/env python
#coding: utf-8

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

class TermStation(db.Model):
    __tablename__ = 'term_station'
    id          =   db.Column(db.Integer, primary_key=True)
    name        =   db.Column(db.String(64))
    address     =   db.Column(db.Integer)
    type_id     =   db.Column(db.Integer,  db.ForeignKey('term_type.id'))
    created_at  =   db.Column(db.DateTime, default=datetime.now)
    updated_at  =   db.Column(db.DateTime)
    
    type = db.relationship('TermType', backref='term_type')
    
class TermType(db.Model):    
    __tablename__ = 'term_type'
    id          =   db.Column(db.Integer, primary_key=True)
    code        =   db.Column(db.String(16))
    name        =   db.Column(db.String(64))
    discr       =   db.Column(db.String(255))
    manu        =   db.Column(db.String(32))
    created_at  =   db.Column(db.DateTime, default=datetime.now)
    updated_at  =   db.Column(db.DateTime)    

    configs = db.relationship('TermConfig',backref='type',lazy='dynamic')
    
class TermConfig(db.Model):
    id          =   db.Column(db.Integer, primary_key=True)
    type_id     =   db.Column(db.Integer,  db.ForeignKey('term_type.id'))
    no          =   db.Column(db.Integer)
    name        =   db.Column(db.String(255))
    measure_type=   db.Column(db.String(8))
    measure_tag =   db.Column(db.String(8))
    measure_coef=   db.Column(db.Float)
    