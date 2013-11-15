# coding: utf-8

from __future__ import absolute_import, unicode_literals


from .utils import *

__all__ = ['BoundRow', 'BoundRows']

## Row
class BoundRow(object):
    def __init__(self, table, record):
        self._table = table
        self._record = record
        self.data = {}
        for column in self.table.columns:
            self.data[column.name] = self.get_value(column.name)
        # print 'BoundRow.__init__()', self.data

    @property
    def table(self):
        return self._table

    @property
    def record(self):
        return self._record

    def show_items(self):
        print len(self.table.columns), ' <--> ', self.table.columns
        for column in self.table.columns:
            print 'show item::', column, '\n', self[column.name], '::'

    @property
    def items(self):
        for bound_column in self.table.columns:
            cellattrs = bound_column.column.cellattrs(bound_column, self.record)
            
            cell = self[bound_column.name]
            name_or_accessor = bound_column.column.accessor \
                               if bound_column.column.accessor else bound_column.name
            if (self.table._meta.group_by and
                self.table._meta.group_by == name_or_accessor):
                group_name = A(self.table._meta.group_by).resolve(self.record)
                if group_name not in self.table.groups:
                    cell = "..."
                else:
                    self.table.groups.remove(group_name)
                    
            yield (bound_column, cell, cellattrs)

    def get_value(self, name):
        bound_column = self.table.columns[name]
        #value = getattr(self.record, name, '')
        value = None
        if bound_column.subcolumns:
            subvalues = []
            for name, field_name in bound_column.subcolumns:
                subvalue = A(field_name).resolve(self.record)
                subvalues.append(str(subvalue))
            value = '/'.join(subvalues)
        elif name not in ['check']:
            try:
                value = bound_column.accessor.resolve(self.record)
            except ValueError, e:
                print e

        kwargs = {
            'value':            lambda: value,
            'record':           lambda: self._record,
            'bound_column':     lambda: bound_column,
            'bound_row':        lambda: self,
            'table':            lambda: self._table,
            }
        render_FOO = 'render_' + bound_column.name
        render = getattr(self.table, render_FOO, bound_column.column.render)
        kw = {}
        for arg_name in bound_column._render_args:
            kw[arg_name] = kwargs[arg_name]()
        return render(**kw)

        
    def __getitem__(self, name):
        return self.data[name]

class BoundRows(object):

    def __init__(self, data):
        self.data = data
        self.rows = []

    def __iter__(self):
        if len(self.rows) == len(self.data):
            for row in self.rows:
                yield row
        else:
            self.rows = []
            table = self.data.table
            for record in self.data:
                row = BoundRow(table, record)
                self.rows.append(row)
                yield row

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return BoundRows(self.data[key])
        else:
            return BoundRow(self.data.table, self.data[key])

