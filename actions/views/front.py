# -*- coding: utf-8 -*-
# coding=utf-8

import web
from .base import ViewsAction
from models.articles import Articles
from models.categories import Categories
from util.log import log
import traceback
from util.utils import counttime


class FrontIndexAction(ViewsAction):
    def __init__(self, name='1'):
        ViewsAction.__init__(self, name)

    def GET(self):
        """
        首页
        :return:
        """
        inputs = self.get_input()
        page = int(inputs.get('page', 1))
        page_size = int(inputs.get('page_size', 20))
        self.private_data['article_list'] = []
        self.private_data['current_page'] = 1
        self.private_data['total_page'] = 0
        self.private_data['category_list'] = []
        try:
            category_list = Categories.select().where(
                Categories.status == 0). \
                order_by(Categories.id.desc())
            article_query = Articles.select().where(Articles.status == 0). \
                order_by(Articles.id.desc())
            article_list = article_query.paginate(page, page_size)
            total_count = article_query.count()
            total_page = (total_count + page_size - 1) / page_size
            self.private_data['article_list'] = article_list.execute()
            self.private_data['current_page'] = page
            self.private_data['total_page'] = total_page
            self.private_data['category_list'] = category_list.execute()
        except Exception as e:
            log.error('Failed to get home data. Error msg %s', e)
            log.error(traceback.format_exc())
        return self.display('front/index')


class FrontAction(ViewsAction):
    def __init__(self, name="1"):
        ViewsAction.__init__(self, name)

    def GET(self, name):
        print("*"*10)
        print(name)
        print("*"*10)
        if not name:
            return web.seeother(self.make_url('/'))
        if name == 'list':
            return self.articles()
        # 文章搜索列表
        elif name == 'search':
            return self.search_list()
        # 文章详情信息
        elif name == 'info':
            return self.article_info()
        elif name == 'article_tag_list':
            return self.article_tag_list()
        elif name == 'about':
            return self.about()
        elif name == 'resume':
            return self.resume()
        else:
            return self.display(name)

    @counttime
    def articles(self):
        """
        文章分类列表
        :return:
        """
        inputs = self.get_input()
        page = int(inputs.get('page', 1))
        page_size = int(inputs.get('page_size', 20))
        category_id = int(inputs.get('category_id', 2))
        self.private_data['article_list'] = []
        self.private_data['current_page'] = 1
        self.private_data['total_page'] = 0
        self.private_data['category_list'] = []
        self.private_data['current_category'] = None
        try:
            category = Categories.get(Categories.id == category_id)
            category_list = Categories.select().where(Categories.status == 0).\
                order_by(Categories.id.desc())

            article_query = Articles.select().where(
                Articles.category == category.id).order_by(Articles.id.desc())
            article_list = article_query.paginate(page, page_size)
            total_count = article_query.count()
            total_page = (total_count + page_size - 1) / page_size
            self.private_data['article_list'] = article_list
            self.private_data['current_category'] = category
            self.private_data['current_page'] = page
            self.private_data['category_list'] = category_list
            self.private_data['total_page'] = total_page
            return self.display('front/article_list')
        except Exception as e:
            log.error('Failed to get category articles data. '
                      'Category_id is %s Error msg %s', category_id, e)
            log.error(traceback.format_exc())
        # return self.error(msg="获取列表信息失败！", url=self.make_url('/views/home'))
        return self.display('front/article_list')

    @counttime
    def search_list(self):
        """
        文章搜索列表
        :return:
        """
        inputs = self.get_input()
        page = int(inputs.get('page', 1))
        page_size = int(inputs.get('page_size', 20))
        keywords = inputs.get('keywords', None)
        self.private_data['article_list'] = []
        self.private_data['current_page'] = 1
        self.private_data['total_page'] = 0
        self.private_data['category_list'] = []
        self.private_data['keywords'] = keywords
        try:
            category_list = Categories.select().where(Categories.status == 0). \
                order_by(Categories.id.desc())
            if keywords:
                article_query = Articles.select().where(
                    Articles.name.contains(keywords))
                total_count = article_query.count()
                total_page = (total_count + page_size - 1) / page_size
                self.private_data['total_page'] = total_page
                self.private_data['current_page'] = page
                self.private_data['category_list'] = category_list
                self.private_data['article_list'] = article_query.\
                    paginate(page, page_size)
                return self.display('front/search_list')
        except Exception as e:
            log.info('Failed to get search result. Keywords is %s. Error msg is',
                     keywords, e)
            log.error(traceback.format_exc())
        return self.display('front/search_list')

    @counttime
    def article_info(self):
        """
        文章详情信息
        :return:
        """
        inputs = self.get_input()
        article_id = int(inputs.get('article_id', 1))
        self.private_data['article'] = None
        self.private_data['category_list'] = []
        try:
            category_list = Categories.select().where(Categories.status == 0). \
                order_by(Categories.id.desc()).execute()
            article = Articles.get(Articles.id == article_id)
            self.private_data['article'] = article
            self.private_data['category_list'] = category_list
            return self.display('front/article_info')
        except Exception as e:
            log.info('Failed to get article info. Article id is %s. Error msg '
                     'is', article_id, e)
            log.error(traceback.format_exc())
        return self.display('front/article_info')

    @counttime
    def about(self):
        """
        文章详情信息
        :return:
        """
        self.private_data['category_list'] = []
        try:
            category_list = Categories.select().where(Categories.status == 0). \
                order_by(Categories.id.desc()).execute()
            self.private_data['category_list'] = category_list
            return self.display('front/about')
        except Exception as e:
            log.info('Failed to get article info.  Error msg '
                     'is', e)
            log.error(traceback.format_exc())
        return self.display('front/about')

    @counttime
    def article_tag_list(self):
        """标签下文章列表:return:"""
        inputs = self.get_input()
        tag = inputs.get('tag', None)
        self.private_data['category_list'] = []
        self.private_data['tag'] = tag
        self.private_data['article_list'] = []
        try:
            category_list = Categories.select().where(Categories.status == 0).\
                order_by(Categories.id.desc())
            if tag:
                article_query = Articles.select().where(Articles.keywords.contains(tag))
                self.private_data['category_list'] = category_list
                self.private_data['article_list'] = article_query.paginate(1, 20)
            return self.display('front/tags_list')
        except Exception as e:
            log.info('Failed to get search result.tag is%s.Error msg is', tag, e)
            log.error(traceback.format_exc())
        return self.display('front/tags_list')    \


    @counttime
    def resume(self):
        """标签下文章列表:return:"""
        self.private_data['category_list'] = []
        try:
            category_list = Categories.select().where(Categories.status == 0).\
                order_by(Categories.id.desc())
            self.private_data['category_list'] = category_list
            return self.display('front/resume')
        except Exception as e:
            log.info('Failed to get search result.tag is%s.Error msg is', e)
            log.error(traceback.format_exc())
        return self.display('front/resume')