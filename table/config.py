# coding: utf-8

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 20

class TableConfig(object):

    def __init__(self, request, profile={}):
        self._request = request
        self._profile = profile

    def configure(self, table):
        table.order_by = self._request.args.get('order_by', None)
        table.hiddens = self._profile.get(table.profile_hiddens_key, '')

        page = int(self._request.args.get('page', DEFAULT_PAGE))
        per_page = int(self._profile.get(table.profile_perpage_key, DEFAULT_PER_PAGE))
        
        table.paginate(page, per_page)
