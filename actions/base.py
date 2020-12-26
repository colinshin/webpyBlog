# -*- coding: utf-8 -*-

import web
from html import parser
from html.parser import HTMLParser
from urllib.parse import urlencode
import json

from tinydb import TinyDB, where

from models.articles import Articles
from models.categories import Categories
from models.friend_link import FriendLink
from models.site import Site
from models.tags import Tags
from settings import config


class BaseAction(object):
    def __init__(self, name):
        self.name = name
        self.globals_tmpl_funcs = {
            'make_url': self.make_url,
            'image_url': self.image_url,
            'static_url': self.static_url,
            'subStr': lambda strings, offset, length: self.sub_text(strings,
                                                                   offset,
                                                                   length),
            'str': lambda x: str(x),
            'htmlunescape': self.htmlunescape,
            'htmlunquote': self.htmlunquote,
            'is_login': self.is_login,
            'get_page_str': self.get_page_str,
            'get_tags': self.get_tags,
            'get_ca_count': self.get_ca_count,
            'get_site_info': self.get_site_info,
            'get_links': self.get_links,
        }

        self.tmpl_dir = None
        self.render = None
        self.private_data = {}

    def make_url(self, url, params=None):
        params_str = '?' + urlencode(params) if params and len(params) > 0 else ''
        return url + params_str

    def image_url(self, image_name):
        return config.STATIC_LOCAL_URL + "/static/%s" % image_name

    def static_url(self, static_name):
        return config.STATIC_LOCAL_URL + "/static/%s" % static_name

    def is_installed(self):
        try:
            from models.version import Version
            return True if Version.table_exists() else False
        except Exception as e:
            return False

    def is_login(self):
        if not hasattr(web.ctx.session, 'user_id'):
            return None
        return web.ctx.session.username

    def set_login(self, username=None, user_id=None):
        if username is None:
            web.ctx.session.username = None
            web.ctx.session.user_id = None
            web.setcookie('user_id', user_id, -10)
        else:
            web.ctx.session.username = username
            web.setcookie('user_id', user_id)

    def validates(self, valid_list):
        user_input = self.get_input()
        for i in valid_list:
            if not i.validate(user_input[i.name]):
                self.error_message = i.note
                return False
        return True

    def sub_text(self, strings, offset, length):
        try:
            decoded = self.strip_tags(strings).lstrip()
            encoded = decoded[offset:length].encode('utf-8')
            if len(decoded) > length:
                encoded += "..."
            return encoded
        except Exception as e:
            return '...'

    def strip_tags(self, html):
        if not html:
            return ""
        html = html.strip()
        html = html.strip("\n")
        result = []
        parse = HTMLParser()
        parse.handle_data = result.append
        parse.feed(html)
        parse.close()
        return "".join(result)

    def get_input(self):
        return self.htmlquote(dict(web.input()))

    def htmlquote(self, input_data):
        if not isinstance(input_data, dict):
            return web.net.htmlquote(input_data)
        else:
            for k, v in input_data.items():
                input_data[k] = self.htmlquote(v)
        return input_data

    def htmlunquote(self, input_data):
        if not isinstance(input_data, dict):
            return web.net.htmlunquote(input_data)
        else:
            for k, v in input_data.items():
                input_data[k] = self.htmlunquote(v)
        return input_data

    def htmlunescape(self, input_data):
        try:
            return parser.unescape(input_data)
        except Exception as e:
            return input_data

    def display(self, tmpl):
        if not self.render:
            return web.nomethod()

        return getattr(self.render, tmpl)(self.private_data)

    def get_page_str(self):
        return ''

    def get_site_info(self):
        return Site.get_or_none(Site.id == 1)

    def get_links(self):
        return FriendLink.select().where(FriendLink.status == 0). \
                order_by(FriendLink.id.asc()).execute()

    def get_ca_count(self, category_id):
        return Categories.select().join(Articles).\
            where(Articles.category.id == int(category_id)).count()

    def get_tags(self):
        db = TinyDB('settings/db.json')
        table = db.table('_default')
        res = table.get(where('name') == 'tags')
        if res:
            data = res.get("data")
            tags_dict_list = json.loads(data)
        else:
            tags_list = Tags.select().where(Tags.status == 0)
            tags_dict_list = []
            for tag in tags_list:
                count = Articles.select().where(Articles.keywords.contains(str(tag.name))).count()
                tags_dict_list.append({tag.name: count})
            db.truncate()
            table = db.table('_default')
            table.insert({"name": "tags", "data": json.dumps(tags_dict_list)})
            db.close()
        return tags_dict_list


class HtmlAction(BaseAction):
    def __init__(self, name):
        BaseAction.__init__(self, name)

    def success(self, msg, url='/', timeout=5):
        self.private_data['JUMP_MSG'] = msg
        self.private_data['JUMP_TIMEOUT'] = timeout
        self.private_data['JUMP_URL'] = url

        return self.display('success')

    def error(self, msg, url='/', timeout=5):
        self.private_data['JUMP_MSG'] = msg
        self.private_data['JUMP_TIMEOUT'] = timeout
        self.private_data['JUMP_URL'] = url

        return self.display('error')

    def back(self, msg, timeout=5):
        self.private_data['JUMP_MSG'] = msg
        self.private_data['JUMP_TIMEOUT'] = timeout

        return self.display('back')

    def notFound(self):
        return self.error(msg='Page not found!')


class JsonAction(BaseAction):
    def __init__(self, name):
        BaseAction.__init__(self, name)

    def success(self, msg=''):
        return json.dumps({})

    # 400
    def error(self):
        return web.BadRequest()

    # 401 用户名或密码错误
    def unauthorized(self):
        return web.webapi.Unauthorized()

    # 403, token非法
    def forbidden(self):
        return web.webapi.Forbidden()

    # 404
    def notFound(self):
        return web.webapi.NotFound()

    # 405, 参数或者方法不正确
    def nomethod(self):
        return web.webapi.NoMethod()

    # 406 您还没有登录
    def notacceptable(self):
        return web.webapi.NotAcceptable()

    # 409 
    def conflict(self):
        return web.webapi.Conflict()

    # 410
    def gone(self):
        return web.webapi.Gone()

    # 412
    def preconditionfailed(self):
        return web.webapi.PreconditionFailed()

    # 415
    def unsupportedmediatype(self):
        return web.webapi.UnsupportedMediaType()
