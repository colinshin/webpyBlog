# -*- coding: utf-8 -*-
# !/usr/bin/env python

from peewee import CharField, DateTimeField, TextField, ForeignKeyField, \
    SmallIntegerField
from datetime import datetime
from models.base import BaseModel
from models.albums import Albums


class FriendLink(BaseModel):
    name = CharField(unique=True)
    link = CharField(null=True)
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)
