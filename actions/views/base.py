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

    def get_page_str(self, url, current_page, total_page=1):
        page_string = ""
        total_page = int(total_page)
        try:
            if total_page == 1:
                return ""
            if '?' in url:
                url = url + '&page='
            else:
                url = url + '?page='

            page_string = '''
            <nav aria-label="Page navigation example">
            <ul class="pagination justify-content-center">
            '''
            if current_page == 1:
                page_string += '''
                <li class="page-item disabled">
                <a class="page-link"href="#"tabindex="-1"aria-disabled="true">上一页</a>
                </li>
                '''
            else:
                page_string += '''<li class="page-item">
                <a class="page-link" href="''' + url + str(current_page - 1) + '''">上一页</a>
                </li>'''
            for i in range(1, total_page + 1):
                page_string += '''<li class="page-item">
                <a class="page-link" href="''' + url + str(i) + '''">''' + str(i) + '''</a>
                </li>'''
            if total_page == current_page:
                page_string += '''
                <li class="page-item disabled">
                <a class="page-link" tabindex="-1" aria-disabled="true" href="#">下一页</a>
                </li>'''
            else:
                page_string += '''<li class="page-item">
                <a class="page-link" href="''' + url + str(current_page + 1) + '''">下一页</a>
                </li>'''
        except Exception as e:
            print(e)
            print(page_string)
        return page_string
