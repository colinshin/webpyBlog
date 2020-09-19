# -*- coding: utf-8 -*-

from peewee import ForeignKeyField, DateTimeField, TextField, SmallIntegerField
from models.base import BaseModel
from models.users import Users
from models.articles import Articles
from datetime import datetime


class ArticleComments(BaseModel):
    owner = ForeignKeyField(Users, related_name='owner_articlecomments',
                            on_delete='CASCADE')
    article = ForeignKeyField(Articles, related_name='article_articlecomments',
                              on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
    content = TextField()
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)
