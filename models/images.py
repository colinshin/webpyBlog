# -*- coding: utf-8 -*-
# !/usr/bin/env python

from peewee import CharField, DateTimeField, TextField, ForeignKeyField, \
    SmallIntegerField
from datetime import datetime
from models.base import BaseModel
from models.albums import Albums


class Images(BaseModel):
    uuid = CharField(unique=True)
    link = CharField(null=True)
    thumbnail = TextField()
    album = ForeignKeyField(Albums, related_name='album_images',
                            on_delete='CASCADE')
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)
