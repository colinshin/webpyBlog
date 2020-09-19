# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from datetime import datetime


class Users(BaseModel):
    cellphone = CharField(unique=True)
    name = CharField()
    nickname = CharField(null=True)
    password = CharField()
    created_time = DateTimeField(default=datetime.now)
    email = TextField(null=True)
    description = TextField()
    address = TextField()
    birthday = TextField()
    avatar = TextField()
    gender = IntegerField()
    status = SmallIntegerField(default=0)

