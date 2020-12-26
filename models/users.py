# -*- coding: utf-8 -*-

from peewee import CharField, TextField, IntegerField, SmallIntegerField, \
    DateTimeField

from models.base import BaseModel
from datetime import datetime


class Users(BaseModel):
    cellphone = CharField(unique=True)
    name = CharField()
    nickname = CharField(null=True)
    password = CharField()
    email = TextField(null=True)
    description = TextField()
    address = TextField()
    birthday = TextField()
    avatar = TextField()
    gender = IntegerField()
    status = SmallIntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)
    updateTime = DateTimeField(default=datetime.now)


