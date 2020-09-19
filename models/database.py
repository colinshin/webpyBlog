# -*- coding: utf-8 -*-
# coding=utf-8

class Database:
    # 先验证数据库是否存在
    def __init__(self):
        self.model_obj = None
        self.model_ = None

    def set_model(self, model_name):
        db_list = __import__('model.' + model_name, {}, {},
                             model_name.capitalize())
        if hasattr(db_list, model_name.capitalize()):
            self.model_ = getattr(db_list, model_name.capitalize())
            self.model_obj = self.model_()

    def fetch_all(self, sql):
        return self.model_.fetch_all(sql)

    def fetch_one(self, **kwargs):
        return self.model_.get_or_none(**kwargs)

    def count_ins(self, **kwargs):
        query = self.model_.select()
        for model_key in kwargs.keys():
            if hasattr(self.model_, model_key):
                model_key_ = getattr(self.model_, model_key)
                query = query.where(model_key_ == kwargs.get(model_key))
        return query.count()

    def insert(self, **kwargs):
        keys = {}
        for model_key in kwargs.keys():
            if hasattr(self.model_, model_key):
                keys.update({model_key: kwargs.get(model_key)})
                instance = self.model_.create(**keys)
                instance.save()
                return instance

    def delete(self, **kwargs):
        instance = self.fetch_one(**kwargs)
        return instance.delete_instance()

    def update(self, condition, **kwargs):
        return self.model_.update(**kwargs).where(condition).excute()

    def execute(self, sql):
        # print(sql)
        return self.model_.execute(sql)

    def get_list(self, orders=None, offset=None, limits=None, **kwargs):
        query = self.model_.select()
        if orders:
            pass
        if offset:
            query = query.offset(offset)
        if limits:
            query = query.limit(limits)
        for model_key in kwargs.keys():
            if hasattr(self.model_, model_key):
                model_key_ = getattr(self.model_, model_key)
                query = query.where(model_key_ == kwargs.get(model_key))
        return query.execute()

    def get_one(self, orders=None, **kwargs):
        query = self.model_
        if orders:
            pass
        for model_key in kwargs.keys():
            if hasattr(self.model_, model_key):
                model_key_ = getattr(self.model_, model_key)
                query = query.get(model_key_ == kwargs.get(model_key))
        return query
