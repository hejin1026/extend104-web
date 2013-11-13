#!/usr/bin/env python
#coding: utf-8

from wtforms.fields import (TextField, PasswordField, HiddenField, BooleanField)
from wtforms import validators
from flask_wtf import Form

class LoginForm(Form):
    username = TextField(u'用户名')
    password = PasswordField(u'密码')
    next     = HiddenField()
    remember = BooleanField(u'记住我')
    
class SignupForm(Form):
    username     = TextField(u'用户名', [validators.InputRequired(), validators.required(u"必填"), validators.length(max=20)])
    email        = TextField(u'邮箱', [validators.Email(u'邮箱格式不正确'), validators.length(max=20)])
    password     = PasswordField(u'密码', [validators.required(u"必填"), validators.EqualTo('password_ack', message=u'密码必须一致')])
    password_ack = PasswordField(u'重复密码', [validators.required(u"必填")])    

class ResetForm(Form):    
    password     = PasswordField(u'密码', [validators.required(u"必填"), validators.EqualTo('password_ack', message=u'密码必须一致')])
    password_ack = PasswordField(u'重复密码', [validators.required(u"必填")])