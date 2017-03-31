#!/usr/bin/env python
#coding=utf-8

from dbmaster.extensions import db


class Querylog(db.Model):
    __tablename__ = 'query_log'
    
    PER_PAGE = 20

    id = db.Column(db.Integer,primary_key=True)

    account_id = db.Column(db.Integer)
    account_name = db.Column(db.String(64))

    op_ip = db.Column(db.String(20))
    op_time = db.Column(db.DateTime)
    content = db.Column(db.Text)
    cost_time = db.Column(db.String(32))



class UpdateApplication(db.Model):
    __tablename__ = 'update_application'

    PER_PAGE = 20

    id = db.Column(db.Integer,primary_key=True)

    account_id = db.Column(db.Integer)
    account_name = db.Column(db.String(64))
    opt_account_id = db.Column(db.Integer)
    opt_account_name = db.Column(db.String(64))
    reason = db.Column(db.String(1024))
    create_time = db.Column(db.DateTime)
    sql_content = db.Column(db.Text)
    status = db.Column(db.Integer)