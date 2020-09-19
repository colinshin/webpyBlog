# -*- coding: utf-8 -*-

from .base import ViewsAction
import web


class IndexAction(ViewsAction):
    def __init__(self, name='1'):
        ViewsAction.__init__(self, name)

    def GET(self):
        return web.seeother(self.make_url('/views/home'))
