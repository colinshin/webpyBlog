# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from datetime import datetime


class Tags(BaseModel):
    name = CharField()
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)

