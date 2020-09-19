# -*- coding: utf-8 -*-

from peewee import TextField
from models.base import BaseModel


class Version(BaseModel):
    description = TextField()
