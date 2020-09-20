# -*- coding: utf-8 -*-

import web
from settings import config
from urllib.parse import urlencode
from actions.base import HtmlAction


class ViewsAction(HtmlAction):
    def __init__(self, name):
        HtmlAction.__init__(self, name)
        self.private_data = {
            'NAME': config.NAME,
            'create_success': False,
        }
        print("*"*20)
        print(name)
        self.tmpl_dir = config.TMPL_DIR
        self.render = web.template.render(self.tmpl_dir,
                                          globals=self.globals_tmpl_funcs)
        self.private_data['render'] = self.render

        if not self.is_installed():
            raise web.seeother(self.make_url('/admin/install'))

    def make_url(self, url, params=None):
        params_str = '?' + urlencode(params) if params and len(params) > 0 else ''
        return url + params_str

    def success(self, msg, url='/views/home', timeout=5):
        return HtmlAction.success(self, msg, url, timeout)

    def error(self, msg, url='/views/home', timeout=5):
        return HtmlAction.error(self, msg, url, timeout)

    def get_page_str(self, url, current_page, page_size, total_count=0):
        page_string = ""
        try:
            total_page = total_count / page_size
            total_page += 1 if total_count % page_size else 0

            if '?' in url:
                url = url + '&page='
            else:
                url = url + '?page='

            page_string = ''

            if current_page > 1:
                page_string += '''
                    <li><a href="''' + url + str(current_page - 1) + '''">←上一页</a></li>
                '''
            if total_page > current_page:
                page_string += '''
                    <li><a href="''' + url + str(current_page + 1) + '''">下一页→</a></li>
               '''
        except Exception as e:
            print(e)
        return page_string

