#!/usr/bin/env python
#coding: utf-8

from wtforms.fields import (TextField, PasswordField, HiddenField, BooleanField)
from wtforms import validators
from flask_wtf import Form

class StationForm(Form):
    name    = TextField(u'名称')
    address = TextField(u'地址')
    type    = TextField(u'类型')
    