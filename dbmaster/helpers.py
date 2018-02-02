#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, print_function

import datetime
from .models import Syslog
from dbmaster.extensions import db


def save_syslog(current_user, op_ip, content):
    syslog = Syslog()
    if current_user.is_authenticated:
        syslog.account_id = current_user.id
        syslog.account_name = current_user.name
    syslog.op_ip = op_ip
    syslog.op_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    syslog.content = content
    db.session.add(syslog)
    db.session.commit()

