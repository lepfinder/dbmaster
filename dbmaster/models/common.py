#!/usr/bin/env python
#coding=utf-8

from dbmaster.extensions import db

class Res():

    def __init__(self,code,message):
        self.code = code
        self.message = message

    def serialize(self):
        return {
            'code' : self.code,
            'message' : self.message
        }


class Syslog(db.Model):
    __tablename__ = 'syslog'
    
    PER_PAGE = 20


    id = db.Column(db.Integer,primary_key=True)

    account_id = db.Column(db.Integer)
    account_name = db.Column(db.String(64))
    op_ip = db.Column(db.String(20))
    op_time = db.Column(db.DateTime)
    content = db.Column(db.Text)