# -*- coding: utf-8 -*-
import decimal
from urllib.request import urlopen

from actions.base import JsonAction
from urllib.parse import urlencode
from config import *
from models.articles import Articles
from models.users import Users
from models.categories import Categories
from models.images import Images
import os, base64
import leancloud
from util.imaging import Imaging
from hashlib import md5
from util.log import log
import urllib2
import utils
import web
import hashlib
import json
import datetime
import time
import random as rand
import traceback


# 获取不是最后一级分类的子分类
def _getchildren(cate, iditem):
    try:
        id_item = iditem
        for item in cate.children:
            _lastcateids(item.id, id_item)
    except Exception:
        return False


# 判断是否是最后一级分类
def _lastcateids(parent, iditem):
    try:
        id_item = iditem
        cate = Categories.select().where(Categories.id == parent)
        for item in cate:
            if item.children.count() == 0:
                id_item.append(item.id)
            elif item.children.count():
                _getchildren(item, id_item)
        return id_item
    except Exception:
        return False


def gen_token():
    r = rand.random()
    return str(hashlib.sha1('%f%s' % (r, time.ctime())).hexdigest())


def post(url, data):
    try:
        req = urllib2.Request(url=url, data=urlencode(data))
        result = urllib2.urlopen(req).read()
        return json.loads(result)
    except Exception as e:
        log.error('execu post %s' % traceback.format_exc())


def get(url, data):
    try:
        params = urlencode(data)
        result = urlopen("%s?%s" % (url, params)).read()
        return result
    except Exception as e:
        log.error('execu get %s' % traceback.format_exc())


class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


counttime = utils.counttime

'''
Web Actions
'''


class ApiAction(JsonAction):
    def __init__(self, name="1"):
        JsonAction.__init__(self, name)

    def GET(self, name):
        # 文章列表
        if name == 'articles':
            return self.articles()
        # 分类列表
        elif name == 'categories':
            return self.categories()
        # 分类列表
        elif name == 'images':
            return self.images()
        # 搜索列表
        elif name == 'search':
            return self.search()
        # 页面,css名称列表
        elif name == 'get_names':
            return self.get_names()
        # 页面,css数据
        elif name == 'get_content':
            return self.get_content()
        else:
            return self.display(name)

    def POST(self, name):
        #  登录
        if name == 'signin':
            return self.signin()
        #  注册
        elif name == 'signup':
            return self.signup()
        #  编辑用户信息
        elif name == 'edit_user_info':
            return self.edit_user_info()
        #  请求api编辑用户信息
        elif name == 'update_user_info':
            return self.update_user_info()
        #  评论文章
        elif name == 'comment_article':
            return self.comment_article()
        #  请求验证码
        elif name == 'request_sms':
            return self.request_sms()

        #  修改用户头像
        elif name == 'update_avatar':
            return self.update_avatar()
        #  文件数据写入
        elif name == 'save_file':
            return self.save_file()

        return self.notFound()

    #   登录实现
    def signin(self):
        try:
            inputs = self.get_input()
            log.info('signin:' + str(inputs))
            cellphone = inputs['cellphone']
            password = md5(inputs['password']).hexdigest()
            user = Users.get(Users.cellphone == cellphone)
            if not user or user.password != password:
                return self.unauthorized()

            t = int(time.time())
            if not user.token or t - time.mktime(
                    user.token_created_time.timetuple()) > 144000:
                token = gen_token()
                user.token = token
                user.token_created_time = datetime.datetime.now()
            else:
                token = user.token
            self.set_login(user.cellphone, token)
            user.last_login_time = datetime.datetime.now()
            user.save()
            return self.success()
        except Exception as e:
            log.error('execs signin %s' % traceback.format_exc())
            return self.unauthorized()

    #   注册实现
    def signup(self):
        inputs = self.get_input()
        try:
            log.info('signup:' + str(inputs))
            cellphone = inputs.get('cellphone')
            smscode = inputs.get('smscode')
            tuser = Users.get(Users.cellphone == cellphone)
            if tuser:
                return self.error()
        except Exception as e:
            log.error('execus signup %s' % traceback.format_exc())
            return self.error()

        try:
            pwd = md5(inputs['password']).hexdigest()

            if not leancloud.Apis().verify_sms_code(cellphone, smscode):
                return self.error()
            signup_token = gen_token()
            created_time = datetime.datetime.now()

            Users.create(
                cellphone=cellphone,
                name=cellphone,
                password=pwd,
                gender=0,
                role=2,
                description=self.htmlunquote(''),
                address="住址",
                token=signup_token,
                token_created_time=created_time,
                birthday="1970-5-12",
                avatur=Images.get(Images.id == 1).thumbnail,
            )
            return self.success()
        except Exception as e:
            log.error('execus signup%s' % traceback.format_exc())
            return self.error()

    #   util
    #   传入uuid返回图片src值
    def __image_uuid(self, uuid):
        try:
            src = None
            image = Images.get(Images.uuid == uuid)

            src = ALI_CDNIMAGES_URL + "/%s" % ALI_OSS_DIR + '/%s.jpeg' % uuid
            log.info('src' + str(src))
            return src
        except Exception as e:
            log.error('__image_uuid %s' % traceback.format_exc())

            #   编辑用户信息

    def edit_user_info(self):
        inputs = self.get_input()
        try:
            user = Users.get(Users.cellphone == self.is_login())

            if inputs.get('name'):
                user.name = inputs['name']

            if inputs.get('description'):
                user.description = self.htmlunquote(inputs['description'])

            if inputs.get('gender'):
                user.gender = int(inputs['gender'])

            if inputs.get('birthday'):
                user.birthday = inputs['birthday']

            if inputs.get('email'):
                user.email = inputs['email']

            user.save()
            return self.success()
        except Users.DoesNotExist:
            log.error('execus edit_user_info %s' % traceback.format_exc())
            return self.forbidden()
        except Exception as e:
            log.error('execus edit_user_info %s' % traceback.format_exc())
            return self.error()

    def articles(self):
        inputs = self.get_input()
        url = API_URL + '/api/articles'
        try:
            log.info('len articles %s' % len(get(url, inputs)))
            return get(url, inputs)
        except Exception as e:
            log.error('execus articles %s' % traceback.format_exc())

    def article_info(self):
        inputs = self.get_input()
        url = API_URL + '/api/article_info'
        try:
            if self.is_login():
                inputs['token'] = Users.get(
                    Users.cellphone == self.is_login()).token
            return get(url, inputs)
        except Exception as e:
            log.error('execus articles %s' % traceback.format_exc())

    def categories(self):
        inputs = self.get_input()
        url = API_URL + '/api/categories'
        try:
            return get(url, inputs)
        except Exception as e:
            log.error('execus categories %s' % traceback.format_exc())

    def images(self):
        inputs = self.get_input()
        url = API_URL + '/api/images'
        try:
            return get(url, inputs)
        except Exception as e:
            log.error('execus images %s' % traceback.format_exc())

    def search(self):
        inputs = self.get_input()
        url = API_URL + '/api/search'
        try:
            return get(url, inputs)
        except Exception as e:
            log.error('execus search %s' % traceback.format_exc())

    def update_user_info(self):
        inputs = self.get_input()
        token = Users.get(Users.cellphone == self.is_login()).token
        inputs['token'] = token
        log.info('inputs %s ' % inputs)
        url = API_URL + '/api/update_user_info'
        try:
            return post(url, inputs)
        except Exception as e:
            log.error('execus update_user_info %s' % traceback.format_exc())

    def comment_article(self):
        inputs = self.get_input()
        token = Users.get(Users.cellphone == self.is_login()).token
        inputs['token'] = token
        url = API_URL + '/api/comment_article'
        try:
            return post(url, inputs)
        except Exception as e:
            log.error('execus comment_article %s' % traceback.format_exc())

    def request_sms(self):
        inputs = self.get_input()
        url = API_URL + '/api/request_sms'
        try:
            return post(url, inputs)
        except Exception as e:
            log.error('execus request_sms %s' % traceback.format_exc())

    def update_avatar(self):
        log.info('into update_avatar')
        _inputs = web.input()
        inputs = {}
        url = API_URL + '/api/update_user_image'

        try:
            token = Users.get(Users.cellphone == self.is_login()).token
            inputs['token'] = token
            log.info('into update_avatar _inputs== %s' % _inputs['pic'])
            log.info('into update_avatar _inputs dir == %s' % dir(_inputs))
            log.info('into update_avatar len ==%s' % len(_inputs))

            import StringIO
            imgstream = StringIO.StringIO(_inputs['pic'])
            im = Imaging(imgstream)
            thumbnail_blob = im.resize(int(im.size()[0] / THUMBNAIL_XRES), \
                                       int(im.size()[1] // THUMBNAIL_YRES))
            thumbnail_data = base64.b64encode(buffer(thumbnail_blob))
            inputs['base64image'] = thumbnail_data
            return post(url, inputs)
        except Exception as e:
            log.info("update_avatar: %s" % traceback.format_exc())
            return self.error()

    def get_names(self):
        inputs = self.get_input()
        log.info('into get_names inputs %s' % inputs)
        module_num = int(inputs['num'])
        temp_names = []
        try:
            urls = TMPL_DIR.replace('desktop1', 'desktop%s' % module_num) + "/"
            temps = os.listdir(urls)
            for item in temps:
                urls = TMPL_DIR.replace('desktop1',
                                        'desktop%s' % module_num) + "/%s" % item
                if item[-4:] == 'html':
                    temp_names.append(
                        {"name": item, "path": urls, "url": WEB_URL})

            return json.dumps(temp_names)
        except Exception as e:
            log.error('get_names%s' % traceback.format_exc())

    def __file_write(self, urls, content):
        try:
            log.info('into __file_write urls: %s,content: %s' % (urls, content))
            file_object = file(urls, 'w')
            # file_object = open(urls,'w')
            file_object.truncate()
            file_object.write(content)
            file_object.close()
        except Exception as e:
            log.error(traceback.format_exc())

    def save_file(self):
        inputs = self.get_input()
        log.info(inputs)
        try:
            filepath = inputs['path']
            text_content = self.htmlunquote(inputs['content']).replace("<<hh>>",
                                                                       "\n")  # content 为编辑之后的内容
            log.info(text_content)
            self.__file_write(filepath, text_content)
            return self.success()
        except Exception as e:
            log.info(traceback.format_exc())
            return self.error()

    def get_content(self):
        inputs = self.get_input()
        log.info('into get_content inputs %s' % inputs)
        filepath = inputs['filepath']
        try:
            if os.path.isfile(filepath):
                fp = open(filepath)
                data = fp.read()
                log.info(data)
            else:
                log.info("not this file")
            return json.dumps({
                'file': data
            })
        except Exception as e:
            log.error(traceback.format_exc())
            return self.error()
        finally:
            fp.close()

    def get_articles_center(self):
        inputs = self.get_input()
        try:
            page = int(inputs['page']) if inputs.has_key('page') else 1
            category_id = inputs['category_id']
            articles = Articles.select().where(
                Articles.category == category_id).order_by(Articles.id.desc())
            return json.dumps([
                {
                    'id': it.id,
                    'name': it.name,
                    'thumbnail': it.thumbnail.thumbnail,
                    'content': self.htmlunquote(it.content),
                } for it in articles.paginate(page, PAGINATE_COUNT_10)])
        except Exception as e:
            log.error('get_articles_center%s' % traceback.format_exc())
            return self.error()
