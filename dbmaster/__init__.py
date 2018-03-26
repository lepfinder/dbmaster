#!/usr/bin/env python
#coding=utf-8
from __future__ import absolute_import, print_function

from flask import Flask,g

from dbmaster import views
from dbmaster.extensions import db, login_manager
from .dbutils import DbUtil

DEFAULT_APP_NAME = 'dbmaster'

DEFAULT_MODULES = (
    (views.dbmaster, "/dbmaster"),
    (views.accounts, "/accounts"),
)


def create_app(config=None, modules=None):

    if modules is None:
        modules = DEFAULT_MODULES   
    
    app = Flask(DEFAULT_APP_NAME)
    
    # config
    app.config.from_pyfile(config)

    configure_extensions(app)
    
    # register module
    configure_modules(app, modules) 

    return app


def configure_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    login_manager.login_message = u"请首先登录。"
    login_manager.login_message_category = "danger"


def configure_modules(app, modules):
    
    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)



