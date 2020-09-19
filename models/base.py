# -*- coding: utf-8 -*-
# !/usr/bin/env python
from abc import ABC

from settings import config
from peewee import SqliteDatabase, MySQLDatabase, Model


class SqliteFKDatabase(SqliteDatabase, ABC):
    def initialize_connection(self, conn):
        self.execute_sql('PRAGMA foreign_keys=ON;')


db = MySQLDatabase(host=config.DB_HOST, user=config.DB_USER,
                   passwd=config.DB_PASSWORD, database=config.DB_NAME,
                   charset='utf8')


class BaseModel(Model):
    class Meta:
        database = db
