# -*- coding: utf-8 -*-

from peewee import CharField, TextField, DateTimeField, SmallIntegerField
from models.base import BaseModel
from datetime import datetime


class Notes(BaseModel):
    name = CharField()
    content = TextField()
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)

