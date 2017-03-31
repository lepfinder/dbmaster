#!/usr/bin/env python
#coding=utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

__all__ = ['db', 'login_manager']

db = SQLAlchemy()
login_manager = LoginManager()