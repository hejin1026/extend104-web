#!/usr/bin/env python
#coding: utf-8

from datetime import datetime

from db import db

class TermStation(db.Model):
    __tablename__ = 'term_station'
    id          =   db.Column(db.Integer, primary_key=True)
    name        =   db.Column(db.String(64))
    address     =   db.Column(db.Integer)
    type_id     =   db.Column(db.Integer,  db.ForeignKey('term_type.id'))
    created_at  =   db.Column(db.DateTime, default=datetime.now)
    updated_at  =   db.Column(db.DateTime)
    
    type = db.relationship('TermType', backref='station_type')
    
class TermStake(db.Model):
    id          =   db.Column(db.Integer, primary_key=True)
    name        =   db.Column(db.String(64))
    address     =   db.Column(db.Integer)
    type_id     =   db.Column(db.Integer,  db.ForeignKey('term_type.id'))
    station_id  =   db.Column(db.Integer,  db.ForeignKey('term_station.id'))
    yc_start    =   db.Column(db.Integer)
    yc_num      =   db.Column(db.Integer) 
    yx_start    =   db.Column(db.Integer) 
    yx_num      =   db.Column(db.Integer) 
    ym_start    =   db.Column(db.Integer)
    ym_num      =   db.Column(db.Integer) 
    yk_start    =   db.Column(db.Integer)
    yk_num      =   db.Column(db.Integer)
    created_at  =   db.Column(db.DateTime, default=datetime.now)
    updated_at  =   db.Column(db.DateTime)
    
    type = db.relationship('TermType', backref='stake_type')  
    station = db.relationship('TermStation', backref='stakes')    
    
class Measure(db.Model):    
    id          =   db.Column(db.Integer, primary_key=True)
    no          =   db.Column(db.Integer)
    category    =   db.Column(db.String(8))
    stake_id    =   db.Column(db.Integer,  db.ForeignKey('term_stake.id'))
    station_id  =   db.Column(db.Integer,  db.ForeignKey('term_station.id'))
    tag         =   db.Column(db.String(8))
    name        =   db.Column(db.String(64))
    code        =   db.Column(db.String(64))
    type        =   db.Column(db.Integer)
    valid       =   db.Column(db.Integer)
    unit        =   db.Column(db.String(8))
    coef        =   db.Column(db.Float)
    offset      =   db.Column(db.Float)
    validUpLmt  =   db.Column(db.Float)
    validDnLmt  =   db.Column(db.Float)
    designValue =   db.Column(db.Float)
    inverse     =   db.Column(db.Integer)
    alarmGrade  =   db.Column(db.Integer)
    flags       =   db.Column(db.Integer)
    
    station = db.relationship('TermStation',backref='mesure')
    stake = db.relationship('TermStake',backref='mesure')
    
    
class TermType(db.Model):    
    __tablename__ = 'term_type'
    id          =   db.Column(db.Integer, primary_key=True)
    code        =   db.Column(db.String(16))
    name        =   db.Column(db.String(64))
    desc        =   db.Column(db.String(255))
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
    
class Channel(db.Model):    
    id          =   db.Column(db.Integer, primary_key=True)
    name        =   db.Column(db.String(64))
    ip          =   db.Column(db.String(32))
    port        =   db.Column(db.Integer)
    protocol_id     =   db.Column(db.Integer,  db.ForeignKey('protocol.id'))
    transmit_type   =   db.Column(db.Integer)    
    channel_type    =   db.Column(db.Integer)
    station_id  =   db.Column(db.Integer,  db.ForeignKey('term_station.id'))
    stake_id    =   db.Column(db.Integer,  db.ForeignKey('term_stake.id'))
    created_at  =   db.Column(db.DateTime, default=datetime.now)  
    
    station = db.relationship('TermStation',backref='channel')
    stake = db.relationship('TermStake',backref='channel')
    
    
class Protocol(db.Model):     
    id          =   db.Column(db.Integer, primary_key=True)
    name        =   db.Column(db.String(64))
    code        =   db.Column(db.String(64))
    desc        =   db.Column(db.String(256))
    
    Channels = db.relationship('Channel',backref='protocol',lazy='dynamic')
    
    