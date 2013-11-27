#!/usr/bin/env python
#coding: utf-8
from jinja2 import Markup
from flask import Blueprint, render_template, request, url_for, flash, redirect

from flask_login import login_required, current_user

from .models import *
from .tables import *
from .forms import StationForm, YCMeasureForm

import httplib

bp = Blueprint('term', __name__)

@bp.before_request
def before_request():
    print 'user.before_request: ', request.endpoint, current_user.is_authenticated(), current_user.is_anonymous()

@bp.route('/term/')
def index():
    
    return redirect(url_for('term.station'))
    
@bp.route('/term/websocket', methods=['GET'])
def websocket():
    sid = request.args.get('id', '') 
    # if not sid:
    webserver = 'ws://localhost:8080/websocket'   
    station = TermStation.query.get(sid)
    kwargs = {
        'station'  : station,
        'webserver': webserver
    }
    return render_template('term/websocket.html', **kwargs)
    

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
        uri = url_for('term.websocket', id=row.record.id)
        row.data['websocket'] =  Markup(u"<a href=%s>%s</a>" % (uri, u'查看'))
        
    kwargs = {
        'table' : table
    }
    return render_template('term/index.html', **kwargs)
    
@bp.route('/station/show',  methods=['GET', 'POST'])
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
    return render_template('term/index.html', **kwargs)
    
@bp.route('/term/measure')
def measure():    
    query = Measure.query
    table = MeasureTable(query).build(request, {})
    kwargs = {
        'table' : table
    }
    return render_template('term/index.html', **kwargs)

@bp.route('/measure/show')
def measure_show():
    id = request.args.get('id', '') 
    form = YCMeasureForm()
    if id:
        measure = Measure.query.filter(Measure.id==id).filter(Channel.channel_type==1).first()
        print 'id:',id, form.name.default, measure.name
        form.no.process_data(measure.no)
        form.name.process_data(measure.name)
        form.stake_name.process_data(measure.stake.name)
        channel = measure.station.channel[0]
        # form.curr_value.process_data()
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        conn.request("GET","/measure?ip=%s&port=%s&measure_type=%s&measure_no=%s" %(channel.ip, channel.port, 1, 0) )
        res = conn.getresponse()
        data = res.read()
        print 'data:',data,res.reason, res.status
        
    
    flash(u"测点信息")
    return render_template('term/measure.html', form = form)

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
    sid = request.args.get('station_id', None)
    bread = []
    if sid:
        query = query.filter(Channel.station_id==sid)
        bread.append((url_for('term.station', id=sid), query.first().station.name))
    table = ChannelTable(query).build(request, {}) 
    
    kwargs = {
        'bread' : bread,
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
    
    