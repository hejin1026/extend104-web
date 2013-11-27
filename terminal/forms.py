#!/usr/bin/env python
#coding: utf-8

from wtforms.fields import (TextField, PasswordField, HiddenField, BooleanField)
from wtforms import validators
from flask_wtf import Form

class StationForm(Form):
    name    = TextField(u'名称')
    address = TextField(u'地址')
    type    = TextField(u'类型')
    
class YCMeasureForm(Form):    
    no      = TextField(u'序号')
    name    = TextField(u'名称')
    category    = TextField(u'类别', default=u'遥测')
    stake_name  = TextField(u'所属桩名')  
    curr_value  = TextField(u'测点值')  
    tag     = TextField(u'标识')
    type    = TextField(u'类型')
    valid   = TextField(u'是否可用')
    unit    = TextField(u'单位')
    coef    = TextField(u'系数')
    offset  = TextField(u'偏移量')
    ValidUpLmt  = TextField(u'有效上限')
    ValidDnLmt  = TextField(u'有效下限')
    DesignValue = TextField(u'设计值')
    Flags   = TextField(u'标志位')
    