# -*- coding: utf-8 -*-
# !/usr/bin/env python

from peewee import CharField, ForeignKeyField, TextField, DateTimeField, \
    SmallIntegerField
from models.base import BaseModel
from models.images import Images
from models.categories import Categories
from datetime import datetime
from .albums import Albums


class Articles(BaseModel):
    name = CharField()
    thumbnail = ForeignKeyField(Images, related_name='thumbnail_articles',
                                on_delete='CASCADE')
    category = ForeignKeyField(Categories, related_name='category_articles',
                               on_delete='CASCADE')
    content = TextField()
    keywords = CharField(max_length=64, null=True)
    summary = TextField(null=True)
    original_address = CharField()
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)
