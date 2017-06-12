#!/usr/bin/env python
# coding=utf-8

import json
import sqlparse
import datetime, time

from flask import Module, Response, request, flash, jsonify, g, current_app, \
    abort, redirect, url_for, render_template

from flask.ext.login import login_required, current_user

from dbmaster.models import  Querylog, Syslog, UpdateApplication
from dbmaster.helpers import save_syslog
from dbmaster.extensions import db
from dbmaster.dbutils import DbUtil
import MySQLdb


dbmaster = Module(__name__)

databases_schema = {}


def loadSchecma():

    schema_sql = """
    SELECT
        TABLE_SCHEMA,
        TABLE_NAME
    FROM
        information_schema.`TABLES`
    WHERE
        TABLE_TYPE != 'SYSTEM VIEW'
    AND TABLE_SCHEMA NOT IN (
        'mysql',
        'performance_schema',
        'information_schema'
    )
    ORDER BY
        TABLE_SCHEMA,
        TABLE_NAME
    """
    result = DbUtil.fetch(schema_sql)

    for d in result:
        # print d[0], d[1]
        if not databases_schema.has_key(d[0]):
            databases_schema[d[0]] = []
        databases_schema[d[0]].append(d[1])


# 首页
@dbmaster.route("/", methods=("GET", "POST"))
@login_required
def index():
    # 查询上次查询的sql
    query_list = Querylog.query.filter_by(account_id=current_user.id).order_by(Querylog.id.desc()).limit(1)

    sql_content = ''
    if query_list:
        sql_content = query_list[0].content
    return render_template("index.html", databases=databases_schema,sql_content = sql_content)


# sql查询历史
@dbmaster.route("/sql_history/", methods=("GET", "POST"))
@login_required
def sql_history():

    query_list = Querylog.query.filter_by(account_id=current_user.id).order_by(Querylog.id.desc()).limit(50)

    return render_template("sql_history.html", query_list=query_list)


# 数据库变更单
@dbmaster.route("/update_application/", methods=("GET", "POST"))
@login_required
def update_application():
    application_list = UpdateApplication.query.filter_by(account_id=current_user.id).order_by(UpdateApplication.id.desc()).limit(50)

    return render_template("update_application.html", application_list=application_list)


# 新建数据库变更单
@dbmaster.route("/new_update_application/", methods=("GET", "POST"))
@login_required
def new_update_application():
    if request.method == "POST":
        reason = request.form['reason']
        sql_content = request.form['sql_content']
        application = UpdateApplication()

        application.account_id = current_user.id
        application.account_name = current_user.name
        application.opt_account_id = current_user.id
        application.opt_account_name = current_user.name
        application.reason = reason
        application.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        application.sql_content = sql_content
        application.status = 0
        db.session.add(application)
        db.session.commit()
        return redirect(url_for("masterview.update_application"))
    else:
        return render_template("new_update_application.html")


# 新建数据库变更单
@dbmaster.route("/audit_sql_application/<int:application_id>", methods=("GET", "POST"))
@login_required
def audit_sql_application(application_id):
    application = UpdateApplication.query.filter_by(id=application_id).first()
    
    sql_content = application.sql_content
    sql_content = sqlparse.format(sql_content,reindent=True)

    return render_template("audit_sql_application.html",application=application,sql_content=sql_content)


@dbmaster.route("/audit_sql_ui/", methods=("GET", "POST"))
@login_required
def audit_sql_ui():
    return render_template("audit_sql.html")


@dbmaster.route("/audit_sql/", methods=("GET", "POST"))
@login_required
def audit_sql():
    try:
        sql_content = request.form['sql_content']

        exec_result = []
        if sql_content:
            print sql_content

            sql='''/*--user=root;--password=123456;--host=11.11.11.12;--enable-execute;--port=3306;*/\
                inception_magic_start;\
                %s
                inception_magic_commit;''' % sql_content
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
                    exec_result.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
                cur.close()
                conn.close()
            except MySQLdb.Error,e:
                         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        return jsonify({
            "code": 200,
            "message": "success",
            "exec_result":exec_result
        })

    except Exception as e:
        print e
        return jsonify({
            "code": 500,
            "message": "%s" % e
        })

# 执行数据库变更
@dbmaster.route("/exec_sql_application/", methods=("GET", "POST"))
@login_required
def exec_sql_application():
    try:
        application_id = request.form['application_id']

        application = UpdateApplication.query.filter_by(id=application_id).first()
        exec_result = []
        if application:
            print application.sql_content

            sql='''/*--user=root;--password=123456;--host=11.11.11.12;--execute=1;--port=3306;*/\
                inception_magic_start;\
                %s
                inception_magic_commit;''' % application.sql_content
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
                    exec_result.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]))
                cur.close()
                conn.close()
            except MySQLdb.Error,e:
                         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        return jsonify({
            "code": 200,
            "message": "success",
            "exec_result":exec_result
        })

    except Exception as e:
        print e
        return jsonify({
            "code": 500,
            "message": "%s" % e
        })

#
@dbmaster.route("/znode_content/", methods=("GET", "POST"))
@login_required
def znode_content():
    if not databases_schema:
        loadSchecma()

    zNodes = []
    for k in databases_schema.keys():
        node = dict({})
        node['name'] = k
        node['open'] = "false"

        children = []

        for table in databases_schema[k]:
            child = dict({})
            child['name'] = table
            children.append(child)
            node['children'] = children

        zNodes.append(node)

    return jsonify({
        "code": 200,
        "message": "success",
        "data": zNodes
    })


#
@dbmaster.route("/hint_content/", methods=("GET", "POST"))
@login_required
def hint_content():
    if not databases_schema:
        loadSchecma()

    hint_options = {}
    for k in databases_schema.keys():
        tables = []
        for table in databases_schema[k]:
            tables.append(table)
        hint_options[k] = tables

    return jsonify({
        "code": 200,
        "message": "success",
        "data": hint_options
    })


# 获取某个表的表结构信息
@dbmaster.route("/table_desc/", methods=("GET", "POST"))
@login_required
def table_desc():

    table_schema = request.form['table_schema']
    table_name = request.form['table_name']

    print "table_desc:",table_schema,table_name
    sql = """
    select ORDINAL_POSITION,COLUMN_NAME,
    COLUMN_TYPE,COLUMN_DEFAULT,IS_NULLABLE,
    CHARACTER_SET_NAME,COLUMN_KEY,COLUMN_COMMENT
    from information_schema.`COLUMNS`
    where TABLE_SCHEMA = '%s' and TABLE_NAME = '%s'
    """ % (table_schema, table_name)
    result = DbUtil.fetch(sql)

    columns = []
    for d in result:
        columns.append(list(d))

    return jsonify({
        "code": 200,
        "message": "success",
        "data": columns
    })


#
@dbmaster.route("/sql_format/", methods=("GET", "POST"))
@login_required
def sql_format():

    sql_content = request.form['sql_content']
    sql_content = sqlparse.format(sql_content,reindent=True)

    print sql_content
    return jsonify({
        "code": 200,
        "message": "success",
        "data": sql_content
    })


@dbmaster.route("/db_execute/", methods=("GET", "POST"))
@login_required
def db_execute():
    result_list = []
    try:
        sql_content = request.form['sql_content']

        sql_arr = sql_content.split(";")

        for sql in sql_arr:
            if sql:
                exec_result = get_exec_result(sql)
                result_list.append(exec_result)

        save_querylog(current_user, request.remote_addr, sql_content, 0)

        return jsonify({
            "code": 200,
            "message": "success",
            "data": result_list
        })

    except Exception as e:
        print e
        return jsonify({
            "code": 500,
            "message": "%s" % e
        })




def get_exec_result(sql_content):
    print "[get_exec_result]", sql_content
    result_set = []
    
    if 'limit' not in sql_content and 'LIMIT' not in sql_content:
        sql_content = "%s limit 200" % sql_content

    t_start = time.time()
    exec_result = DbUtil.fetch(sql_content)
    t_end = time.time()
    cost_time = "%5s" % "{:.4f}".format(t_end - t_start)

    print "[db_execute]sql_content = %s,cost time %s" % (sql_content,cost_time)
    cursor = exec_result.cursor
    titles = cursor.description
    for i in exec_result:
        l = list(i)
        l2 = []
        for j in l:
            # 有些日期格式的转换为字符串输出到前台
            if isinstance(j,datetime.datetime):
                l2.append(j.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                l2.append(j)
        result_set.append(l2)


    result = {
       "titles": titles,
       "result_set": result_set,
       "rowcount": cursor.rowcount,
       "cost_time": cost_time
    }

    #print "[get_exec_result]", result

    return result


# 保存查询记录
def save_querylog(current_user, op_ip, content,cost_time):
    querylog = Querylog()
    if current_user.is_authenticated:
        querylog.account_id = current_user.id
        querylog.account_name = current_user.name
    querylog.op_ip = op_ip
    querylog.op_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    querylog.content = content
    querylog.cost_time = cost_time
    db.session.add(querylog)
    db.session.commit()


# 关于页
@dbmaster.route("/about/", methods=("GET", "POST"))
def about():
    return render_template("about.html")


# 查看操作日志
@dbmaster.route("/syslog/", methods=("GET", "POST"))
@dbmaster.route("/syslog/<int:page>/", methods=("GET", "POST"))
def syslog(page=1):
    page_obj = Syslog.query.order_by(Syslog.id.desc()).paginate(page, Syslog.PER_PAGE, False)

    return render_template("syslog.html", page_obj=page_obj)
