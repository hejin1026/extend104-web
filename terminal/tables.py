#!/usr/bin/env python
#coding: utf-8

from table import tables as t

from .models import *


class StationTable(t.Table):
    
    show = t.Action(name=u'查看', endpoint='term.station_show')
    edit = t.Action(name=u'编辑', endpoint='term.station_edit')
    delete = t.Action(name=u'删除', endpoint='term.station_del')

    check = t.CheckBoxColumn()
    
    name        = t.LinkColumn(u'名称',endpoint='term.station_show')
    address     = t.Column(u'地址')
    type_name   = t.Column(u'类型', accessor='type.name')
    stake_count = t.LinkColumn(u'充电桩或终端',endpoint='term.stake')
    created_at  = t.DateTimeColumn(u'创建时间', orderable=True)
    chanel_count= t.Column(u'通道数量')
    websocket   = t.Column(u'报文')
    
    class Meta:
        model = TermStation
        

class StakeTable(t.Table):
    name        = t.Column(u'名称')
    address     = t.Column(u'地址')
    type_name   = t.Column(u'类型', accessor='type.name')
    station_name   = t.Column(u'所属站', accessor='station.name')
    measure     = t.LinkColumn(u'所属测点', endpoint='term.measure')
    yc_start    = t.Column(u'遥测起始', accessor='yc_start') 
    yc_num      = t.Column(u'遥测总数') 
    yx_start    = t.Column(u'遥信起始') 
    yx_num      = t.Column(u'遥信总数') 
    ym_start    = t.Column(u'遥脉起始') 
    ym_num      = t.Column(u'遥脉总数') 
    yk_start    = t.Column(u'遥控起始') 
    yk_num      = t.Column(u'遥控总数') 
    created_at  = t.DateTimeColumn(u'创建时间', orderable=True)

    class Meta:
        model = TermStake       
        

class MeasureTable(t.Table):
    no          = t.LinkColumn(u'序号', endpoint='term.measure_show')
    name        = t.Column(u'名称')
    code        = t.Column(u'代号')
    category    = t.Column(u'类别')
    stake_name  = t.Column(u'所属终端', accessor='stake.name')
    tag         = t.Column(u'标识')
    type        = t.Column(u'类型')
    valid       = t.EnumColumn(u'是否可用', '', enums={0:u'否', 1:u'是'}, orderable=True)
        
    class Meta:
        model = Measure
            
        
class TypeTable(t.Table):       
    name        = t.Column(u'名称')
    desc        = t.Column(u'描述')
    
    class Meta:
        model = TermType
        
class ConfigTable(t.Table):        
    no          = t.Column(u'序号')
    name        = t.Column(u'名称')
    type_name   = t.Column(u'终端类型',  accessor='type.name')
    measure_type    = t.Column(u'型号')
    measure_tag     = t.Column(u'标识')
    measure_coef    = t.Column(u'系数')
    
    class Meta:
        model = TermConfig
        
class ChannelTable(t.Table):        
    name        = t.Column(u'名称')
    ip          = t.Column(u'IP')
    port        = t.Column(u'端口')
    protocol_name   = t.Column(u'协议', accessor='protocol.name')
    transmit_type   = t.Column(u'传输类型')
    channel_type    = t.Column(u'通道类型')
    station_name    = t.Column(u'所属站', accessor='station.name')
    stake_name      = t.Column(u'所属桩', accessor='stake.name')
    created_at      = t.DateTimeColumn(u'创建时间', orderable=True)
    
    class Meta:
        model = Channel

class ProtocolTable(t.Table):    
    name        = t.Column(u'名称')
    desc        = t.Column(u'描述')    
    
    class Meta:
        model = Protocol
        
