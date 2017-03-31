#!/usr/bin/env python
# coding=utf-8

from flask import current_app
from dbmaster.extensions import db


class DbUtil():

    def __init__(self):
        pass

    @staticmethod
    def fetch(sql_content):
        return db.session.execute(sql_content, bind=db.get_engine(current_app, bind="read"))

