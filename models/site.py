# -*- coding: utf-8 -*-
from peewee import CharField, DateTimeField

from models.base import BaseModel
from datetime import datetime


class Site(BaseModel):
    username = CharField()
    position = CharField()
    case_number = CharField()
    copyright = CharField()
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)
