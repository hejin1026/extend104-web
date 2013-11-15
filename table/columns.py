# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from itertools import  islice
import datetime

from jinja2 import Markup
from jinja2.filters import escape
from flask import url_for

from .utils import *

__all__ = ['Column', 'EnumColumn', 'CheckBoxColumn', 'BaseLinkColumn', 'LinkEnumColumn', 'LinkColumn',
           'EmailColumn', 'DateTimeColumn', 'BoundColumn', 'BoundColumns','PopoverColumn']

## Column
class Column(object):
    creation_counter = 0

    def __init__(self, verbose_name=None, attrs=None, accessor=None, subcolumns=None,
                  orderable=None, ifnull=None):
        if not (accessor is None or isinstance(accessor, basestring) or
                callable(accessor)):
            raise TypeError('accessor must be a string or callable, not %s' %
                            type(accessor).__name__)
        if callable(accessor) and default is not None:
            raise TypeError('accessor must be string when default is used, not callable')
        self.accessor = A(accessor) if accessor else None

        self.verbose_name = verbose_name
        self.subcolumns = subcolumns
        self.orderable = orderable
        self.ifnull = ifnull

        # default_attrs = Attrs(th={'class': 'manage-column', 'scope': 'col'})
        default_attrs = Attrs(th={}, td={})
        attrs = attrs or Attrs()
        if not isinstance(attrs, Attrs):
            warnings.warn('attrs must be Attrs object, not %s'
                          % type(attrs).__name__, DeprecationWarning)
            attrs = Attrs(attrs)
        default_attrs.update(attrs)
        self.attrs = default_attrs
        
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1
        # print 'Column.creation_counter', Column.creation_counter

    
    def cellattrs(self, bound_column, record):
        return {}

    def render(self, value, record=None, bound_column=None):
        if value == None and self.ifnull != None:
            return self.ifnull
        else:
            return value


class EnumColumn(Column):
    def __init__(self, verbose_name, name, enums=None, attrs=None, **extra):
        super(EnumColumn, self).__init__(verbose_name, attrs=attrs, **extra)
        self.name = name
        self.enums = enums

    def cellattrs(self, bound_column, record):
        return {'class': 'enum-%s' % bound_column.accessor.resolve(record)}

    def render(self, value, record, bound_column):
        if value in self.enums:
            return self.enums[value]
        return value

        
class CheckBoxColumn(Column):

    def __init__(self, attrs=None, **extra):
        attrs = attrs or Attrs()
        if not isinstance(attrs, Attrs):
            warnings.warn('attrs must be Attrs object, not %s'
                          % type(attrs).__name__, DeprecationWarning)
            attrs = Attrs(td__input=attrs)

        kwargs = {b'orderable': False, b'attrs': attrs}
        kwargs.update(extra)
        super(CheckBoxColumn, self).__init__(**kwargs)

        
    @property
    def header(self):
        default = {'type': 'checkbox'}
        general = self.attrs.get('input')
        specific = self.attrs.get('th__input')
        attrs = AttributeDict(default, **(specific or general or {}))
        return Markup(u'<input %s/>' % attrs.as_html())


    def render(self, record, bound_column):  # pylint: disable=W0221
        default = {
            'type': 'checkbox',
            'name': 'id',
            'value': record.id
        }
        general = self.attrs.get('input')
        specific = self.attrs.get('td__input')
        attrs = AttributeDict(default, **(specific or general or {}))
        return Markup(u'<input %s/>' % attrs.as_html())


class BaseLinkColumn(Column):

    def __init__(self, verbose_name, attrs=None, *args, **kwargs):
        attrs = attrs or Attrs()
        if not isinstance(attrs, Attrs):
            warnings.warn('attrs must be Attrs object, not %s'
                          % type(attrs).__name__, DeprecationWarning)
            attrs = Attrs(a=attrs)
        kwargs[b'attrs'] = attrs
        # print 'BaseLinkColumn.attrs:', attrs
        super(BaseLinkColumn, self).__init__(verbose_name, *args, **kwargs)

    def render_link(self, uri, text, attrs=None):
        attrs = AttributeDict(attrs if attrs is not None else
                              self.attrs.get('a', {}))
        html = u'<a href="{uri}"{attrs}>{text}</a>'.format(
            uri=escape(uri),
            attrs=" %s" % attrs.as_html() if attrs else "",
            text=escape(text)
        )
        return Markup(html)


class LinkColumn(BaseLinkColumn):

    def __init__(self, verbose_name, endpoint=None, values=None, _external=None,
                 attrs=None, **extra):
        # print 'LinkColumn.attrs:', attrs
        super(LinkColumn, self).__init__(verbose_name, attrs=attrs, **extra)
        self.endpoint = endpoint
        self.values = values
        self._external = _external


    def render(self, value, record, bound_column):
        if not self.endpoint and not bound_column.url_maker:
            raise ValueError('An *endpoint* or *url_maker* is required')

        params = {}
        if self.endpoint:
            params[b'endpoint'] = self.endpoint

        # DEFAULT: has it's `id` as query_string
        record_id = getattr(record, 'id', None)
        if record_id:
            params['id'] = record_id

        if self.values:
            for key, val in self.values.items():
                params[key] = val

        if self._external:
            params[b'_external'] = self._external

        uri = None
        if bound_column.url_maker:
            uri = bound_column.url_maker(record)
        else:
            uri = url_for(**params)
        return self.render_link(uri, value)


class LinkEnumColumn(LinkColumn):
    def __init__(self, verbose_name, enums=None, attrs=None, **extra):
        self.enums = enums
        super(LinkEnumColumn, self).__init__(verbose_name, attrs=attrs, **extra)

    def cellattrs(self, bound_column, record):
        return {'class': 'enum-%s' % bound_column.accessor.resolve(record)}
        
    def render(self, value, record=None, bound_column=None):
        if value not in self.enums:
            raise ValueError('Invalid enmu value, <%r: %r>' % (value, self.enums))
        else:
            value = self.enums[value]
        return super(LinkEnumColumn, self).render(value, record, bound_column)
    

class EmailColumn(BaseLinkColumn):
    def render(self, value):
        return self.render_link("mailto:%s" % value, value)

class PopoverColumn(BaseLinkColumn):
    def render(self, value, record=None, bound_column=None):
        html = u'<button rel="popover" class="btn btn-small" data-content="{content}" data-original-title="{title}" data-placement="bottom">{text}</button>'.format(
            content=escape(value),
            title=escape(record.module.replace('<','').replace('>','')),
            text=escape(bound_column.verbose_name)
        )
        return Markup(html)

class DateTimeColumn(Column):
    def __init__(self, verbose_name, format='%Y-%m-%d %H:%M:%S', *args, **extra):
        super(DateTimeColumn, self).__init__(verbose_name, *args, **extra)
        self.format = format

    def render(self, value):
        if value is None:
            return ''
        if not isinstance(value, datetime.datetime):
            raise TypeError('The value must a *datetime.datetime* type')
        return value.strftime(self.format)


class BoundColumn(object):
    def __init__(self, table, column, name):
        self.table = table
        self.column = column
        self.subcolumns = column.subcolumns
        self.name = name
        self.is_checkbox = True if isinstance(column, CheckBoxColumn) else False

        url_makers = getattr(table._meta, 'url_makers', None)
        self.url_maker = url_makers.get(name, None) if url_makers else None
        

    @property
    def header(self):
        # 通过 column_header = self.column.header 来获取表头的值
        # 会导致意想不到的错误
        column_header = getattr(self.column, 'header', None)
        if column_header is not None:
            return column_header

        verbose_name = self.verbose_name
        return Markup(title(verbose_name))

    @property
    def subcolumns_header(self):
        verbose_names = [verbose_name for verbose_name, field_name in self.subcolumns]
        return Markup(title(' / '.join(verbose_names)))
        
    @property
    def accessor(self):
        """ Name or accessor"""
        return self.column.accessor or A(self.name)


    @property
    def verbose_name(self):
        if self.column.verbose_name:
            return self.column.verbose_name

        name = self.name.replace('_', ' ')
        return name

    @property
    def attrs(self):
        # Work on a copy of the Attrs object since we're tweaking stuff
        attrs = dict(self.column.attrs)
        # print 'attrs:', attrs

        # Find the relevant th attributes (fall back to cell if th isn't
        # explicitly specified).
        attrs["td"] = td = AttributeDict(attrs.get('td', attrs.get('cell', {})))
        attrs["th"] = th = AttributeDict(attrs.get("th", attrs.get("cell", {})))
        # make set of existing classes.
        th_class = set((c for c in th.get("class", "").split(" ") if c))
        td_class = set((c for c in td.get("class", "").split(" ") if c))
        # add classes for ordering
        if not self.is_checkbox:
            th['id'] = self.name
        if getattr(self, 'hidden', None):
            th["style"] = "display: none;"
            td["style"] = "display: none;"
        if self.orderable:
            th_class.add("orderable")
            th_class.add("sortable")

        order_by = getattr(self.table, 'order_by', None)
        if order_by and (order_by == self.name
                         or order_by[1:] == self.name):
            th_class.add('desc' if order_by[0] == '-' else 'asc')
        # Always add the column name as a class
        th_class.add(self.name + '-column')
        td_class.add(self.name + '-column')

        if th_class:
            th['class'] = " ".join(sorted(th_class))
        if td_class:
            td['class'] = " ".join(sorted(td_class))
        return attrs


    @property
    def orderable(self):
        return self.column.orderable


class BoundColumns(object):                   # dict
    def __init__(self, table):
        self.table = table
        self.columns = SortedDict()
        for name, column in self.table.base_columns.iteritems():
            self.columns[name] = BoundColumn(self.table, column, name)

        for name, bound_column in self.iteritems():
            bound_column.render = bound_column.column.render
            bound_column._render_args = getargspec(bound_column.render).args[1:]
            # print 'bound_column._render_args::', bound_column._render_args

    def iteritems(self):
        # print self.table.sequence
        for name in self.table.sequence:
            yield (name, self.columns[name])

    def __len__(self):
        return len(self.columns)


    def iterall(self):
        return (self.columns[name] for name in self.table.sequence)


    def __iter__(self):
        for name in self.table.sequence:
            yield self.columns[name]

    def __getitem__(self, index):
        if isinstance(index, int):
            try:
                return next(islice(self.iterall(), index, index + 1))
            except StopIteration:
                raise IndexError
        elif isinstance(index, basestring):
            for bound_column in self.iterall():
                if bound_column.name == index:
                    return bound_column
            raise KeyError("Column with name '%s' does not exist; "
                           "choices are: %s" % (index, self.table.sequence))
        else:
            raise TypeError(u'row indices must be integers or str, not %s'
                            % type(index).__name__)

