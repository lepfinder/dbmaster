#!/usr/bin/env python
#coding=utf8
import MySQLdb
sql='''/*--user=root;--password=123456;--host=11.11.11.12;--execute=1;--port=3306;*/\
    inception_magic_start;\
    use test;\
    CREATE TABLE qd_user(id int comment 'test' primary key,user_name varchar(32) default '' not null comment 'user name') engine=innodb DEFAULT CHARSET=utf8mb4 comment '测试';\
    inception_magic_commit;'''
#print sql
try:
        conn=MySQLdb.connect(host='11.11.11.10',user='',passwd='',db='',port=6669)
        cur=conn.cursor()
        ret=cur.execute(sql)
        result=cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print field_names
        for row in result:
                print row[0], "|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",row[5],"|",row[6],"|",row[7],"|",row[8],"|",row[9],"|",row[10]
        cur.close()
        conn.close()
except MySQLdb.Error,e:
             print "Mysql Error %d: %s" % (e.args[0], e.args[1])