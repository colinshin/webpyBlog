# -*- coding: utf-8 -*-

from peewee import CharField, TextField, DateTimeField
from models.base import BaseModel
from datetime import datetime


class Notes(BaseModel):
    name = CharField()
    content = TextField()
    created_time = DateTimeField(default=datetime.now)
