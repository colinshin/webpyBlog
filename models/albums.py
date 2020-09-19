# -*- coding: utf-8 -*-


from peewee import CharField, TextField, ForeignKeyField
from models.base import BaseModel
from models.users import Users


class Albums(BaseModel):
    name = CharField()
    description = TextField()
    thumbnail = TextField()
    owner = ForeignKeyField(Users, related_name='owner_albums',
                            on_delete='CASCADE')
