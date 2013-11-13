#!/usr/bin/env python
#coding: utf-8

from flask import Blueprint, render_template, request

from flask_login import login_required, current_user

from .models import TermStation, TermType, TermConfig

bp = Blueprint('term', __name__)

@bp.before_request
def before_request():
    print 'user.before_request: ', request.endpoint, current_user.is_authenticated(), current_user.is_anonymous()

@bp.route('/term/')
@login_required
def index():
    title = "test web"
    station = TermStation.query.all()
    table = {
        'columns': [u"名称", u"地址", u"类型"],
        'rows': station
    }
    return render_template('term/index.html', title = title, table = table)

@bp.route('/term/station')
def station():
    return render_template('station.html')

@bp.route('/term/stake')
def stake():
    return render_template('stake.html')    

@bp.route('/term/type')
def type():
    station = TermType.query.all()
    table = {
        'columns': [u"名称", u"描述", u"所属站点"],
        'rows': station
    }
    return render_template('term/type.html', table = table)


@bp.route('/term/config')
def config():
    station = TermConfig.query.all()
    table = {
        'columns': [u"类型", u"终端号", u"名称", u"指标类型", u"指标标志", u"指标偏移"],
        'rows': station
    }
    return render_template('term/config.html', table = table)
    
    