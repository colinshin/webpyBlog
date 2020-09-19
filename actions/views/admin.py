# -*- coding: utf-8 -*-
# coding=utf-8

import web
from .base import ViewsAction
from util.pwd_util import admin_pwd_digest
from models.articles import Articles
from models.users import Users
from models.categories import Categories

from util.log import log
from util import utils
import hashlib
import json
import time
import random as rand
import urllib
import traceback


# 获取不是最后一级分类的子分类
def _getchildren(cate, iditem):
    try:
        iditem = iditem
        for item in cate.children:
            _lastcateids(item.id, iditem)
    except Exception:
        return False


# 判断是否是最后一级分类
def _lastcateids(parent, iditem):
    try:
        iditem = iditem
        cate = Categories.select().where(Categories.id == parent)
        for item in cate:
            if item.children.count() == 0:
                iditem.append(item.id)
            elif item.children.count():
                _getchildren(item, iditem)
        return iditem
    except Exception:
        return False


def get(url, data):
    try:
        params = urllib.urlencode(data)
        result = urllib.urlopen("%s?%s" % (url, params)).read()
        return json.loads(result)
    except Exception as e:
        log.error('execu get %s' % traceback.format_exc())


def gen_token():
    r = rand.random()
    return str(hashlib.sha1('%f%s' % (r, time.ctime())).hexdigest())


counttime = utils.counttime

'''
Web Actions
'''


class AdminAction(ViewsAction):
    def __init__(self, name="1"):
        ViewsAction.__init__(self, name)

    def GET(self, name):
        if not name:
            return self.login()
        #   首页
        if name == 'login':
            return self.login()
        #   退出
        elif name == 'signout':
            return self.signout()
        #   资讯中心
        elif name == 'home':
            return self.home()
        #   文章列表
        elif name == 'articles':
            return self.articles()
        elif name == 'category_list':
            return self.category_list()
        #   文章搜索列表
        elif name == 'create_article':
            return self.create_article()
        #   中心服务文章列表
        elif name == 'update_article':
            return self.update_article()
        #   用户信息
        elif name == 'delete_article':
            return self.delete_article()
        #   编辑用户信息
        elif name == 'edit_user_info':
            return self.edit_user_info()
        #   中心服务文章列表
        elif name == 'create_category':
            return self.create_category()
        #   用户信息
        elif name == 'update_category':
            return self.update_category()
        else:
            return self.display(name)

    def POST(self, name):
        if not name:
            return self.login()
        if name == 'create_article':
            return self.create_article()
        #   中心服务文章列表
        elif name == 'update_article':
            return self.update_article()
        #   编辑用户信息
        elif name == 'edit_user_info':
            return self.edit_user_info()
        #   中心服务文章列表
        elif name == 'create_category':
            return self.create_category()
        #   用户信息
        elif name == 'update_category':
            return self.update_category()
        else:
            return self.display(name)

    @counttime
    def login(self):
        inputs = self.get_input()
        username = inputs.get("username", None)
        password = inputs.get("password", None)
        if not username or password:
            self.private_data["error_msg"] = "用户名和密码不能为空！"
            return self.display("login")
        user = Users.get(Users.name == username)
        if user.password != admin_pwd_digest(password):
            self.private_data["error_msg"] = "用户名或密码错误！"
            return self.display("login")
        self.set_login(username, user.id)
        self.private_data['user'] = user
        return web.seeother(self.make_url('/admin/home'))

    @counttime
    def home(self):
        inputs = self.get_input()
        return self.display('admin/index')

    #   退出登录
    @counttime
    def signout(self):
        self.set_login(None, None)
        return web.seeother(self.make_url('admin/login'))

    def category_list(self):
        inputs = self.get_input()
        page = int(inputs.get('page', 1))
        page_size = int(inputs.get('page_size', 20))
        self.private_data['current_page'] = page
        self.private_data['total_page'] = 0
        self.private_data['category_list'] = []
        try:
            category_query = Categories.select().where(Categories.status == 0).\
                order_by(Categories.id.desc())
            total_count = category_query.count()
            total_page = (total_count + page_size - 1) / page_size
            self.private_data['category_list'] = \
                category_query.paginate(page, page_size).execute()
            self.private_data['total_page'] = total_page
            return self.display("admin/category_list")
        except Exception as e:
            log.error('Failed to get category list data. Error msg %s', e)
            log.error(traceback.format_exc())
        return self.display('admin/category_list')

    @counttime
    def articles(self):
        inputs = self.get_input()
        page = int(inputs.get('page', 1))
        page_size = int(inputs.get('page_size', 20))
        self.private_data['current_page'] = page
        self.private_data['total_page'] = 0
        self.private_data['article_list'] = []
        try:
            article_query = Articles.select().where(Articles.status == 0)\
                .order_by(Articles.id.asc())
            total_count = article_query.count()
            total_page = (total_count + page_size - 1) / page_size
            self.private_data['total_page'] = total_page
            self.private_data['article_list'] = \
                article_query.paginate(page, page_size).execute()
            return self.display('admin/article_list')
        except Exception as e:
            log.error('Failed to get article list data. Error msg %s', e)
            log.error(traceback.format_exc())
            return self.display('admin/article_list')
    #
    # def __get_c_article(self, c_id):
    #     c_article = [{
    #         'id': item.id,
    #         'name': item.name,
    #         'thumbnail': item.thumbnail.thumbnail,
    #         'content': item.content,
    #         'brief': item.extended
    #     } for item in
    #         Articles.select().where(Articles.category == c_id).limit(5)]
    #     return c_article
    #
    # #   资讯中心
    # @counttime
    # def update_article(self):
    #     inputs = self.get_input()
    #     categories = 0
    #     self.private_data['ARTICLES'] = None
    #     self.private_data['CATEGORIES'] = None
    #     try:
    #         page = int(inputs['page']) if inputs.has_key('page') else 1
    #         category_id = inputs['category_id']
    #         cate_ids = _lastcateids(INFOMATION_CATEGORY_ID, [])
    #         if cate_ids:
    #             self.private_data['CATEGORIES'] = Categories.select().where(
    #                 Categories.id << cate_ids)
    #         articles = Articles.select().where(
    #             Articles.category == category_id).order_by(Articles.id.desc())
    #         self.private_data['TOTAL_PAGE'] = Articles.select().where(
    #             Articles.category == category_id).count() / PAGINATE_COUNT_10
    #         self.private_data['CURRENT_PAGE'] = page
    #         self.private_data['CURRENT_CATEGORY'] = category_id
    #         self.private_data['ARTICLES'] = ([
    #             {
    #                 'id': it.id,
    #                 'name': it.name,
    #                 'created_time': it.createTime,
    #                 'brief': it.extended,
    #                 'thumbnail': it.thumbnail.thumbnail,
    #                 'content': self.htmlunquote(it.content),
    #             } for it in articles.paginate(page, PAGINATE_COUNT_10)])
    #     except Exception as e:
    #         log.error('articles_center %s' % traceback.format_exc())
    #         pass
    #
    #     try:
    #         return self.display('news_list')
    #     except Exception as e:
    #         log.error('articles_center %s' % traceback.format_exc())
    #         return self.error(msg='获取资讯中心页面失败', url=self.make_url('/views/home'))
    #
    # #   最新公告
    # @counttime
    # def delete_article(self):
    #     inputs = self.get_input()
    #     page = int(inputs['page']) if inputs.has_key('page') else 1
    #     category_id = inputs['category_id'] if inputs.has_key(
    #         'category_id') else None
    #     try:
    #         category = Categories.get(Categories.id == category_id)
    #         articles = Articles.select()
    #         articlesList = articles \
    #             .order_by(Articles.id.desc()) \
    #             .paginate(page, PAGINATE_COUNT_12)
    #         self.private_data['ARTICLES'] = articlesList
    #
    #         self.private_data['PAGE_STRING'] = self.get_page_str(
    #             self.make_url('/views/articles_new',
    #                          {'category_id': category_id}), page,
    #             PAGINATE_COUNT_12, articles.count())
    #         return self.display('announcements')
    #     except Exception as e:
    #         log.error('articles_new %s' % traceback.format_exc())
    #         return self.error(msg='获取最新公告页面失败', url=self.make_url('/views/home'))
    #
    # #   用户信息
    # @counttime
    # def user_info(self):
    #     try:
    #         user = Users.get(Users.cellphone == self.is_login())
    #         self.private_data['USER'] = user
    #         return self.display('personal_data')
    #     except Exception as e:
    #         log.error('user_info %s' % traceback.format_exc())
    #         return self.error(msg='获取用户信息页面失败', url=self.make_url('/views/home'))
    #
    # #   文章搜索列表
    # @counttime
    # def asearch_list(self):
    #     inputs = self.get_input()
    #     page = int(inputs['page']) if inputs.has_key('page') else 1
    #     keywords = inputs['keywords'] if inputs.has_key('keywords') else None
    #     self.private_data['TOTAL_PAGE'] = 0
    #     self.private_data['ARTICLES'] = ([])
    #     self.private_data['CURRENT_PAGE'] = 0
    #     articles = None
    #     try:
    #         if keywords:
    #             keywords = keywords.replace('，', ',')
    #             list = keywords.split(',')
    #             for keyword in list:
    #                 articles = Articles.select() \
    #                     .where(Articles.name.contains(keyword))
    #
    #             self.private_data[
    #                 'TOTAL_PAGE'] = articles.count() / PAGINATE_COUNT_12
    #             self.private_data['CURRENT_PAGE'] = page
    #             self.private_data['ARTICLES'] = ([
    #                 {
    #                     'id': it.id,
    #                     'name': it.name,
    #                     'time': it.createTime,
    #                     'extended': it.extended,
    #                     'thumbnail': it.thumbnail.thumbnail,
    #                 } for it in articles.paginate(page, PAGINATE_COUNT_12)])
    #             log.info('into asearch_list %s' % self.private_data['ARTICLES'])
    #             return self.display('news_search')
    #     except Exception as e:
    #         log.error(traceback.format_exc())
    #     return self.display('news_search')
    #
    # #   更多资讯列表
    # @counttime
    # def create_category(self):
    #     inputs = self.get_input()
    #     page = int(inputs.get('page', 1))
    #     category_id = inputs.get('category_id', None)
    #     try:
    #         if category_id:
    #             category = Categories.get(Categories.id == category_id)
    #         else:
    #             category = Categories.get(
    #                 Categories.id == [i.id for i in
    #                                   Categories.select().where(
    #                                       Categories.parent == 2)][0])
    #         categories = Categories.select().where(
    #             Categories.parent == category.id)
    #         if not categories.count():
    #             categories = Categories.select().where(
    #                 Categories.parent == category.parent)
    #     except Exception as e:
    #         log.error(traceback.format_exc())
    #         return self.error(msg="当前没有分类数据,请先录入数据！",
    #                           url=self.make_url('/views/home'))
    #
    #     try:
    #         articles = Articles.select().where(
    #             Articles.category == category.id).order_by(Articles.id.desc())
    #         self.private_data['PAGE_STRING'] = self.get_page_str(
    #             self.make_url('/views/articles_service',
    #                          {'category_id': category_id}), page,
    #             PAGINATE_COUNT, articles.count())
    #         self.private_data['ARTICLES'] = articles.paginate(page,
    #                                                       PAGINATE_COUNT)
    #         self.private_data['CATEGORY'] = category
    #         self.private_data['CATEGORY_NAME'] = category.name
    #         self.private_data['CATEGORIES'] = categories
    #         self.private_data['INTERFACE'] = 'articles_service'
    #         return self.display('services')
    #     except Exception as e:
    #         log.error(traceback.format_exc())
    #         return self.error(msg="获取列表信息失败！", url=self.make_url('views/home'))
    #
    # #   文章详情信息
    # @counttime
    # def update_category(self):
    #     inputs = self.get_input()
    #     article_id = inputs.get('article_id')
    #     page = inputs.get('page', 1)
    #     article = Articles.get(Articles.id == article_id)
    #     article_comments = ArticleComments.select().where(
    #         ArticleComments.article == article_id).order_by(
    #         ArticleComments.id.desc())
    #     self.private_data['PAGE_STRING'] = self.get_page_str(
    #         self.make_url('/views/article_info', {'article_id': article_id}),
    #         page, PAGINATE_COUNT, article_comments.count())
    #
    #     self.private_data['ARTICLE_COMMENTS'] = ([{
    #         'id': item.id,
    #         'name': item.owner.name,
    #         'created_time': item.created_time,
    #         'thumbnail': item.owner.avatur,
    #         'content': self.htmlunquote(item.content),
    #     } for item in article_comments.paginate(page, PAGINATE_COUNT)])
    #     self.private_data['ARTICLE'] = article
    #     self.private_data['ARTICLE_UUID'] = article.thumbnail.uuid + '.jpeg'
    #     return self.display('news_details')
    #
    # #   编辑用户
    # @counttime
    # def edit_user_info(self):
    #     try:
    #         user = Users.get(Users.cellphone == self.is_login())
    #         self.private_data['USER'] = user
    #         return self.display('edit_personal_data')
    #     except Exception as e:
    #         log.error('edit_user_info %s' % traceback.format_exc())
    #         return self.error(msg='编辑用户信息失败', url=self.make_url('/views/home'))
    #
    # #   custom
    # #   文章列表
    # @counttime
    # def custom_articles(self):
    #     inputs = self.get_input()
    #     page = inputs.get('page', 1)
    #     try:
    #         articles = Articles.select()
    #         self.private_data['PAGE_STRING'] = self.get_page_str(
    #             self.make_url('/views/custom_articles'), page, PAGINATE_COUNT,
    #             articles.count())
    #         categories = Categories.select().where(
    #             Categories.id << [article.category.id for article in articles])
    #         self.private_data['CATEGORIES'] = categories
    #         articles = Articles.select().paginate(page, PAGINATE_COUNT)
    #         self.private_data['ARTICLES'] = articles
    #         return self.display('articles_list')
    #     except Exception as e:
    #         log.error('custom_articles' % traceback.format_exc())
    #         return self.error(msg="获取文章列表信息失败！",
    #                           url=self.make_url('/views/home'))
    #
    # #   分类下文章列表
    # @counttime
    # def category_articles(self):
    #     inputs = self.get_input()
    #     page = int(inputs.get('page', 1))
    #     category = int(inputs['category_id'])
    #     try:
    #         articles = Articles.select()
    #         self.private_data['PAGE_STRING'] = self.get_page_str(
    #             self.make_url('/views/category_articles'), page,
    #             PAGINATE_COUNT, articles.count())
    #         articles = Articles.select().where(Articles.category == category)
    #         self.private_data['ARTICLES'] = articles.paginate(page,
    #                                                       PAGINATE_COUNT)
    #         return self.display('news_list')
    #     except Exception as e:
    #         log.error('category_articles %s' % traceback.format_exc())
    #         return self.error(msg="获取文章列表信息失败！",
    #                           url=self.make_url('/views/home'))
    #
    # def update_category(self):
    #     pass
    #
    # def create_article(self):
    #     pass
