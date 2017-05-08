## 介绍
dbmaster是一个python编写的在线数据库查询客户端，可以有效隔离线上数据库环境，提供了一系列便于开发者使用的特性。操作体验尽量兼容navcat。
github地址：https://github.com/lepfinder/dbmaster

## 特性
1. 支持SQL语法高亮和自动提示
2. 支持SQL格式化
3. 支持执行选中的SQL片段
4. 支持数据库SCHEMA显示和表结构信息（双击表名显示表结构信息）
5. 支持快捷键执行，Cmd+R/Ctrl+R执行SQL
6. 支持查询执行记录
7. 支持多个语句同时执行，显示多个result结果集


## 安装和启动

```
git clone  https://github.com/lepfinder/dbmaster.git
cd dbmaster/

pip install virtualenv

下载代码

git clone https://github.com/lepfinder/dbmaster.git


# 激活虚拟环境
virtualenv venv
. venv/bin/activate

# 安装依赖
pip install -r requirments.txt

# 创建和初始化数据库
db.sql

# 配置数据库连接
config.cfg

# 启动服务器
gunicorn -w 4 -b 127.0.0.1:8880 wsgi:application

访问: http://localhost:8880/dbmaster/
```

### 支持的快捷键

注意光标在编辑器的时候才会触发。

- Ctrl+R / Cmd+R 执行sql
- Ctrl+F / Cmd+F 格式化当前编辑器的sql



### 运行效果图
![](http://7xo9p3.com1.z0.glb.clouddn.com/markdown/1490931779997.png?imageMogr2/thumbnail/!100p/quality/100!)

![](http://7xo9p3.com1.z0.glb.clouddn.com/markdown/1490931809868.png?imageMogr2/thumbnail/!100p/quality/100!)

![](http://7xo9p3.com1.z0.glb.clouddn.com/markdown/1490922673923.png?imageMogr2/thumbnail/!100p/quality/100!)


### 相关辅助插件
实现这个客户端用到了一些前后端的开源框架和组件，都是非常优秀的产品，特别感谢这些软件的开发者和维护者。

#### Bootstrap
http://v3.bootcss.com/


#### SQL语法高亮和自动提示
http://codemirror.net/index.html


#### sql美化
http://sqlparse.readthedocs.io/en/latest/intro/#getting-started
```
$ pip install sqlparse
$ python
>>> import sqlparse
>>> print(sqlparse.format('select * from foo', reindent=True))
select *
from foo
>>> parsed = sqlparse.parse('select * from foo')[0]
>>> parsed.tokens
[<DML 'select' at 0x7f22c5e15368>, <Whitespace ' ' at 0x7f22c5e153b0>, <Wildcard '*' … ]
>>>
```

#### Ztree 渲染数据库和表列表
http://www.treejs.cn/v3/main.php#_zTreeInfo


## TODO
- 保存当前查询sql为模板,配置图表渲染
- 线上数据库变更申请流程

## 一些参考资料
http://www.cnblogs.com/Ray-liang/p/4837850.html

如果你有什么好的想法，欢迎告诉我（sdlgxxy@qq.com）





