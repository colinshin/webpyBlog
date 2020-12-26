# -*- coding: utf-8 -*-
# !/usr/bin/env python
from datetime import datetime

from peewee import CharField, TextField, ForeignKeyField, SmallIntegerField, \
    DateTimeField
from models.base import BaseModel


class Categories(BaseModel):
    name = CharField(unique=True)
    thumbnail = TextField()
    description = TextField()
    # Self-referential foreign keys should always be null=True.
    parentName = CharField(null=True)
    parent = ForeignKeyField('self', null=True, related_name='children')
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)

