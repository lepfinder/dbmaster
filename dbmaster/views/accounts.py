#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, print_function

import datetime

from flask import Module, Response, request, flash, jsonify, g, current_app, \
    abort, redirect, url_for, session, render_template

from flask.ext.login import login_user, logout_user, current_user

from dbmaster.models import  Account
from dbmaster.extensions import db, login_manager
from dbmaster.helpers import save_syslog

accounts = Module(__name__)

# 注册
@accounts.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    login_name = request.form['login_name']
    name = request.form['name']
    passwd = request.form['passwd']

    checkAccount = Account.query.filter_by(login_name=login_name).first()

    if checkAccount:
        flash("the username has already exists,please change another one.", 'danger')
    else:
        account = Account(login_name, name, passwd)
        account.create_time = datetime.datetime.now().strftime('%Y-%d-%d %H:%M:%S')

        db.session.add(account)
        db.session.commit()

        flash(u"register success,please login first.", "info")

    return redirect(url_for("accounts.login"))


# 加载用户
@login_manager.user_loader
def load_user(userid):
    account = Account.query.filter_by(id=userid).first()
    return account


# 用户登录
@accounts.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_name = request.form['login_name']
        password = request.form['password']

        if login_name:
            account = Account.query.filter_by(login_name=login_name).filter_by(passwd=password).first()

            if account:
                if login_user(account):
                    save_syslog(account, request.remote_addr, u"登录成功")

                    return redirect(request.args.get("next") or url_for("masterview.index"))
            else:
                flash("Sorry, please check your username or password!", "danger")

        else:
            flash("Sorry, please check your username or password!", "danger")
    return render_template("login.html")


# 用户登录
@accounts.route("/oa_login/", methods=["GET", "POST"])
def oa_login():
    login_name = ''
    name = ''
    if request.method == "POST":
        login_name = request.form['login_name']
        name = request.form['name'].encode("utf-8")
    else:
        login_name = request.args.get('login_name', '')
        name = request.args.get('name', '').encode("utf-8")
    print ("oa_login,login_name =", login_name, ",name =", name)

    if login_name and name:
        account = Account.query.filter_by(login_name=login_name).first()

        if not account:  # 如果不存在，首先创建用户，然后默认登录
            account = Account(login_name, name, '123456')
            account.create_time = datetime.datetime.now().strftime('%Y-%d-%d %H:%M:%S')

            db.session.add(account)
            db.session.commit()

            save_syslog(account, request.remote_addr, u"创建用户")

        if login_user(account):
            save_syslog(account, request.remote_addr, u"登录成功")

            return redirect(request.args.get("next") or url_for("books.index"))

    return redirect(request.args.get("next") or url_for("masterview.index"))


# 用户登出
@accounts.route("/logout/")
def logout():
    save_syslog(current_user, request.remote_addr, u"登出")

    logout_user()

    flash(u"已退出登录.", 'info')
    return redirect(url_for("masterview.index"))
