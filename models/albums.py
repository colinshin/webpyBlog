# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import CharField, SmallIntegerField, DateTimeField
from models.base import BaseModel


class Albums(BaseModel):
    name = CharField()
    is_show = SmallIntegerField(default=0)
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)
