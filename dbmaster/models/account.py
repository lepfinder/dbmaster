#!/usr/bin/env python
#coding=utf-8

from flask.ext.login import UserMixin
from dbmaster.extensions import db


class Account(db.Model,UserMixin):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(64))
    login_name = db.Column(db.String(64))
    mobile = db.Column(db.String(64))
    passwd = db.Column(db.String(64))
    city = db.Column(db.String(64))
    create_time = db.Column(db.DateTime)

    def __init__(self,login_name,name,passwd):
        self.login_name = login_name
        self.name = name
        self.passwd = passwd


