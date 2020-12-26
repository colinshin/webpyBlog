# -*- coding: utf-8 -*-
# coding=utf-8
from time import time
from functools import wraps
import web
from tinydb import TinyDB

from models.albums import Albums
from models.site import Site
from models.tags import Tags
from .base import ViewsAction
from util.pwd_util import admin_pwd_digest
from models.articles import Articles
from models.users import Users
from models.categories import Categories
from models.images import Images

from util.log import log
from util import utils
import traceback

counttime = utils.counttime


def login_required(func):
    def decorated(*args, **kwargs):
        if not web.ctx.session.username:
            return web.seeother('login')
        return func(*args, **kwargs)

    return decorated


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
        elif name == 'logout':
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
        elif name == 'albums_list':
            return self.albums_list()
        elif name == 'create_album':
            return self.create_album()
        elif name == 'update_album':
            return self.update_album()
        elif name == 'save_site_info':
            return self.save_site_info()
        else:
            return self.display(name)

    def POST(self, name):
        if not name:
            return self.login()
        if name == 'login':
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
        elif name == 'create_album':
            return self.create_album()
        elif name == 'update_album':
            return self.update_album()
        elif name == 'save_site_info':
            return self.save_site_info()
        else:
            return self.display(name)

    @login_required
    @counttime
    def home(self):
        return self.display('admin/index')

    @counttime
    def login(self):
        self.private_data["error_msg"] = None
        if web.ctx.method == "GET":
            return self.display("admin/login")
        else:
            inputs = self.get_input()
            username = inputs.get("username", None)
            password = inputs.get("password", None)
            res = (not username) or (not password)
            if res:
                self.private_data["error_msg"] = "用户名和密码不能为空！"
                return self.display("admin/login")
            user = Users.get_or_none(Users.name == username)
            if not user:
                self.private_data["error_msg"] = "用户名或密码错误！"
                return self.display("admin/login")
            if user.password != admin_pwd_digest(password):
                self.private_data["error_msg"] = "用户名或密码错误！"
                return self.display("admin/login")
            self.set_login(username, user.id)
            self.private_data['user'] = user
            return web.seeother(self.make_url('home'))

    #   退出登录
    @counttime
    def signout(self):
        self.set_login(None, None)
        return web.seeother(self.make_url('login'))

    @login_required
    def category_list(self):
        inputs = self.get_input()
        page = int(inputs.get('page', 1))
        page_size = int(inputs.get('page_size', 20))
        self.private_data['current_page'] = page
        self.private_data['total_page'] = 0
        self.private_data['category_list'] = []
        try:
            category_query = Categories.select().where(Categories.status == 0). \
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
    @login_required
    def articles(self):
        inputs = self.get_input()
        page = int(inputs.get('page', 1))
        page_size = int(inputs.get('page_size', 20))
        self.private_data['current_page'] = page
        self.private_data['total_page'] = 0
        self.private_data['article_list'] = []
        try:
            article_query = Articles.select().where(Articles.status == 0) \
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

    @counttime
    @login_required
    def create_article(self):
        if web.ctx.method == "GET":
            category_list = Categories.select().where(Categories.status == 0)
            self.private_data["category_list"] = category_list
            return self.display("admin/create_article")
        else:
            inputs = self.get_input()
            title = inputs.get('name')
            content = inputs.get('content')
            summary = inputs.get("summary")
            category_id = inputs.get("category_id")
            source_url = inputs.get("source_url", "")
            keywords = str(inputs.get("keywords", "")).strip()
            image = Images.get_or_none()
            category = Categories.get_or_none(Categories.id == category_id)
            try:
                tags_list = keywords.split("，") if keywords else []
                if tags_list:
                    got_tags = Tags.select().where(Tags.name.in_(tags_list))
                    tmp_list = []
                    for tag in got_tags:
                        tmp_list.append(tag.name)
                    for tag_str in tags_list:
                        if tag_str not in tmp_list:
                            t = Tags(name=tag_str)
                            t.save()
                    db = TinyDB('settings/db.json')
                    db.truncate()
                    db.close()
                article = Articles(name=title, content=content,
                                   summary=summary,
                                   category=category,
                                   original_address=source_url,
                                   keywords=keywords,
                                   thumbnail=image)
                article.save()
                self.private_data["create_success"] = True
                return web.seeother(self.make_url('articles'))
            except Exception as e:
                log.error('create article failed %s' % traceback.format_exc())
                log.error('input params %s' % inputs)
                self.private_data["create_success"] = False
                return self.display("admin/create_article")

    @counttime
    @login_required
    def update_article(self):
        inputs = self.get_input()
        if web.ctx.method == "GET":
            article_id = inputs.get("article_id")
            category_list = Categories.select().where(Categories.status == 0)
            article = Articles.get_or_none(Articles.id == article_id)
            print(article.id)
            self.private_data["article"] = article
            self.private_data["category_list"] = category_list
            return self.display("admin/update_article")
        else:
            article_id = inputs.get("article_id")
            name = inputs.get('name')
            content = inputs.get('content')
            summary = inputs.get("summary")
            category_id = inputs.get("category_id")
            source_url = inputs.get("source_url", "")
            keywords = str(inputs.get("keywords", "")).strip()
            article = Articles.get_or_none(Articles.id == article_id)
            try:
                tags_list = keywords.split("，") if keywords else []
                if tags_list:
                    got_tags = Tags.select().where(Tags.name.in_(tags_list))
                    tmp_list = []
                    for tag in got_tags:
                        tmp_list.append(tag.name)
                    for tag_str in tags_list:
                        tag_str.strip()
                        if tag_str not in tmp_list:
                            t = Tags(name=tag_str)
                            t.save()
                    db = TinyDB('settings/db.json')
                    db.truncate()
                    db.close()
                article.update(name=name, content=content, summary=summary,
                               category_id=category_id,
                               original_address=source_url,
                               keywords=keywords,
                               updateTime=time()).where(Articles.id ==
                                                        article_id).execute()
                self.private_data["update_success"] = True
                return web.seeother(self.make_url('articles'))
            except Exception as e:
                log.error('update article failed %s' % traceback.format_exc())
                log.error('input params %s' % inputs)
                self.private_data["update_success"] = False
                return web.seeother(self.make_url('update_article'))

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

    @login_required
    @counttime
    def create_category(self):
        if web.ctx.method == "GET":
            category_list = Categories.select().where(Categories.status == 0)
            self.private_data["category_list"] = category_list
            return self.display("admin/create_category")
        else:
            inputs = self.get_input()
            name = inputs.get('name')
            desc = inputs.get('desc')
            parent_id = inputs.get("parent_id")
            try:
                category = Categories(name=name,
                                      description=desc,
                                      parent_id=parent_id)
                category.save()
                self.private_data["create_success"] = True
                return web.seeother(self.make_url('category_list'))
            except Exception as e:
                log.error('create category failed %s' % traceback.format_exc())
                log.error('input params %s' % inputs)
                self.private_data["create_success"] = False
                return self.display("admin/create_category")

    @login_required
    @counttime
    def update_category(self):
        inputs = self.get_input()
        if web.ctx.method == "GET":
            category_id = inputs.get("category_id")
            category = Categories.get_or_none(Categories.id == category_id)
            category_list = Categories.select().where(Categories.status == 0)
            self.private_data["category"] = category
            self.private_data["category_list"] = category_list
            return self.display("admin/update_category")
        else:
            category_id = inputs.get('category_id')
            name = inputs.get('name')
            desc = inputs.get('desc')
            parent_id = inputs.get("parent_id")
            category = Categories.get_or_none(Categories.id == category_id)
            try:
                category.update(name=name,
                                description=desc,
                                parent_id=parent_id). \
                    where(Categories.id == category_id).execute()
                self.private_data["create_success"] = True
                return web.seeother(self.make_url('category_list'))
            except Exception as e:
                log.error('update category failed %s' % traceback.format_exc())
                log.error('input params %s' % inputs)
                self.private_data["update_success"] = False
                return self.display("admin/update_category")

    @login_required
    @counttime
    def albums_list(self):
        inputs = self.get_input()
        if web.ctx.method == "GET":
            page = int(inputs.get('page', 1))
            page_size = int(inputs.get('page_size', 20))
            self.private_data['current_page'] = page
            self.private_data['total_page'] = 0
            albums_query = Albums.select().where(Albums.status == 0).\
                order_by(Albums.id.asc())
            total_count = albums_query.count()
            total_page = (total_count + page_size - 1) / page_size
            self.private_data['total_page'] = total_page
            self.private_data['albums_list'] =\
                albums_query.paginate(page, page_size).execute()
            return self.display("admin/albums_list")

    @login_required
    @counttime
    def create_album(self):
        inputs = self.get_input()
        if web.ctx.method == "POST":
            name = inputs.get('name', '').strip()
            album = Albums.get_or_none(Albums.name == name)
            if album:
                self.private_data["create_success"] = False
                self.private_data["create_message"] = u"相册已存在"
                return self.display("admin/create_album")
            try:
                album = Albums(name=name)
                album.save()
                self.private_data["create_success"] = True
                self.private_data["create_message"] = u"相册创建成功"
                return web.seeother(self.make_url('albums_list'))
            except Exception as e:
                log.error('create album failed%s' % traceback.format_exc())
                self.private_data["create_success"] = False
                self.private_data["create_message"] = u"创建相册失败"
                return self.display("admin/create_album")
        if web.ctx.method == "GET":
            return self.display("admin/create_album")

    @login_required
    @counttime
    def update_album(self):
        inputs = self.get_input()
        if web.ctx.method == "POST":
            name = inputs.get('name', '').strip()
            album_id = inputs.get("album_id", None)
            exist_album = Albums.get_or_none(Albums.name == name)
            if exist_album and exist_album.id != album_id:
                self.private_data["update_success"] = False
                self.private_data["update_message"] = u"同名相册已存在"
                return web.seeother(self.make_url('update_album',
                                                  {'album_id': album_id}))
            try:
                album = Albums.get_or_none(Albums.id == int(album_id))
                if album:
                    Albums.update(name=name, updateTime=time()).\
                    where(Albums.id == int(album_id)).execute()
                    self.private_data["update_success"] = True
                    return web.seeother(self.make_url('albums_list'))
            except Exception as e:
                log.error('create album failed%s' % traceback.format_exc())
                self.private_data["update_success"] = False
                self.private_data["update_message"] = u"更新相册失败"
                return web.seeother(self.make_url('update_album',
                                                  {'album_id': album_id}))
        if web.ctx.method == "GET":
            album_id = inputs.get("album_id",None)
            if not album_id or not album_id.isdigit():
                self.private_data["update_success"] =False
                self.private_data["update_message"] = u"参数有误"
                return web.seeother(self.make_url('albums_list'))
            album = Albums.get_or_none(Albums.id == int(album_id))
            if not album:
                return web.seeother(self.make_url('albums_list'))
            self.private_data["album"] = album
            return self.display("admin/update_album")

    # #   编辑用户
    # @counttime
    # def edit_user_info(self):
    #     try:
    #         user = Users.get(Users.cellphone == self.is_login())
    #         self.private_data['USER'] = user
    #         return self.display('edit_personal_data')
    #     except Exception as e:
    #         log.error('edit_user_info %s' % traceback.format_exc())
    #         return self.error(msg='编辑用户信息失败', url=self.make_url('/views/home'))    # #   编辑用户


    @counttime
    def save_site_info(self):
        inputs = self.get_input()
        if web.ctx.method == "POST":
            username = inputs.get('username', '').strip()
            position = inputs.get('position', '').strip()
            case_number = inputs.get('case_number', '').strip()
            copy_right = inputs.get("copyright", '').strip()
            try:
                Site.update(username = username,
                                      position=position,
                                      case_number=case_number,
                                      copyright=copy_right).\
                    where(Site.id == 1).execute()
                self.private_data["update_success"] = True
                return web.seeother(self.make_url('home'))
            except Exception as e:
                log.error('create album failed%s' % traceback.format_exc())
                self.private_data["update_success"] = False
                self.private_data["update_message"] = u"更新失败"
                return web.seeother(self.make_url('save_site_info'))
        if web.ctx.method == "GET":
            site = Site.get_or_none(Site.id == 1)
            self.private_data["site"] = site
            return self.display("admin/site_info")
