#!/usr/bin/env python
#coding: utf-8
from jinja2 import Markup
from flask import Blueprint, render_template, request, url_for, flash, redirect

from flask_login import login_required, current_user

from .models import *
from .tables import *
from .forms import StationForm

bp = Blueprint('term', __name__)

@bp.before_request
def before_request():
    print 'user.before_request: ', request.endpoint, current_user.is_authenticated(), current_user.is_anonymous()

@bp.route('/term/')
def index():
    
    return redirect(url_for('term.station'))
    
@bp.route('/term/websocket')
def websocket():
    sid = request.args.get('id', '') 
    station = TermStation.query.get(sid)
    kwargs = {
        'ip'    : station.ip,
        'table' : table
    }
    return render_template('term/station.html', **kwargs)
    

@bp.route('/term/station')
def station():
    query =  TermStation.query
    table = StationTable(query).build(request, {})
    for row in table.rows:        
        print 'staion_id:',row['stake_count'], row.record.id          
        count = TermStake.query.filter(TermStake.station_id==row.record.id).count()        
        uri = url_for('term.stake', station_id=row.record.id)
        row.data['stake_count'] = Markup(u"<a href=%s>%s</a>" % (uri, count))
        count = Channel.query.filter(Channel.station_id==row.record.id).count()
        uri = url_for('term.channel', station_id=row.record.id)
        row.data['chanel_count'] = Markup(u"<a href=%s>%s</a>" % (uri, count))
        
    kwargs = {
        'table' : table
    }
    return render_template('term/station.html', **kwargs)
    
@bp.route('/term/station/show',  methods=['GET', 'POST'])
def station_show():
    sid = request.args.get('id', '') 
    form = StationForm()
    if sid:
        station = TermStation.query.get(sid)
        print 'sid:',sid, form.name.default, station.name
        form.name.process_data(station.name)
        form.address.process_data(station.address)
        form.type.process_data(station.type.name)
        
    flash(u"站点信息")
    return render_template('term/show.html', form = form)    

@bp.route('/term/stake')
def stake():
    sid = request.args.get('station_id', None)
    query =  TermStake.query
    if sid:
        query = query.filter(TermStake.station_id==sid)
    station = request.args.get('station', '')    
    if station:
        query = query.join(TermStation).filter(TermStation.name == (u'%s' % station))
         
    table = StakeTable(query).build(request, {})
          
    kwargs = {
        'table' : table,
        'station' : station
    }
    return render_template('term/stake.html', **kwargs)


# term_config

@bp.route('/term/type')
def type():
    query = TermType.query
    table = TypeTable(query).build(request, {})
        
    kwargs = {
        'table' : table
    }
    return render_template('term/config.html', **kwargs)


@bp.route('/term/config')
def config():
    query = TermConfig.query
    table = ConfigTable(query).build(request, {})
    
    kwargs = {
        'table' : table
    }
    return render_template('term/config.html', **kwargs)
    
@bp.route('/term/channel')
def channel():
    query = Channel.query
    table = ChannelTable(query).build(request, {})
    
    kwargs = {
        'table' : table
    }
    return render_template('term/config.html', **kwargs)    

@bp.route('/term/protocol')
def protocol():
    query = Protocol.query
    table = ProtocolTable(query).build(request, {})
    
    kwargs = {
        'table' : table
    }
    return render_template('term/config.html', **kwargs)        
    
    