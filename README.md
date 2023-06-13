# 9900-backend
前后端分离的项目，后端使用：Flask RESTx + SQLite3 + SQLAlchemy

### Dependencies
1. **Flask RESTx：** 是 Flask-restfull 的升级版，是 flask 框架开发接口的一个框架，可以生成 swagger 在线文档。
2. **SQLite**: 一个小型 SQL 数据库实现，非常容易启动和运行。请记住，您可能想在生产环境中考虑更可靠的数据库，例如 PostgreSQL 或 MySQL。
3. **Flask-SQLAlchemy**：Flask 扩展添加了对 SQLAlchemy 的支持，这是一种对象关系映射器，使我们更容易与 SQL 数据库进行交互。


要在 Flask 项目中设置 SQLAlchemy，可以导入 flask_sqlalchemy 软件包，然后将 Flask app 变量包装在新的 SQLAlchemy 对象。我们还希望在 Flask 应用程序配置中设置 SQLALCHEMY_DATABASE_URI 以指定我们要使用的数据库以及如何访问它。

### Structure
1. **app.py:** 后端项目的主要文件，启动该文件则开启后端 flask 服务
2. **instance/test.db:** 后端数据库，SQLite
3. **requirements.txt:** 涉及到所有的 packages 及其版本
4. **test.py:** 写一些不放在 app.py 中运行的测试代码，如删除数据库，SQL语句等
5. **practice.py:** 练习代码，可以用来测试收发 http 请求等

### Run service
2 ways:

1. pycharm run file
2. terminal: python3 app.py

## 文档

Swagger 文档

### 其他
导出 python 项目所有依赖包： `pip3 freeze > requirements.txt `