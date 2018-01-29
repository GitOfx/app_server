# -*- coding: utf-8 -*-
# http://docs.jinkan.org/docs/flask/
'''
#sqlite3.connect(dbName) will create the db if not exists
# http://www.pythondoc.com/flask-sqlalchemy/index.html

'''
import sys,logging
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, url_for, render_template,request,session,g,redirect,abort,flash
from app.db.user_db import Table_user

from app.data_model.base_model import *
# import flask_sqlalchemy
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Importing flask.ext.sqlalchemy is deprecated, use flask_sqlalchemy instead.

# create our flask application
app = Flask(__name__)
#mysql://scott:tiger@localhost/mydatabase   dialect+driver://username:password@host:port/database
mysql = "mysql+pymysql://root:root@localhost:3306/alchemy_app_news"
app.config['SQLALCHEMY_DATABASE_URI'] = mysql #'sqlite:///alchemy_app_news.db'
alchemy_db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")
# CRITICAL	50ERROR	40WARNING	30INFO	20DEBUG	10 NOTSET	0

@app.route('/')
def domain():
    '''
    show welcome page
    '''
    return render_template('domain.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/android')
def android():
    return render_template('android.html')

@app.route('/register', methods=['POST'])
def add_entry():
    user_name = request.form['username']
    password = request.form['password']
    user = Table_user()
    result = user.insert_user(user_name,password)
    all_user = user.selectAll()
    if result:
        return render_template('registered.html',user = all_user)
    else:
        flash('New entry was successfully posted')
        errorstr = "rigister fail"
        return render_template('error.html',error = errorstr)
     
@app.route('/login', methods=['GET', 'POST'] )
def login():
    error = None
    form = request.form
    print(form)
    user_name = request.form['username']
    password = request.form['password']
    user = Table_user()
    result = user.select_user(user_name,password)
    error = "login success"
    if len(result) <=0 :
       error = 'login fail'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# @app.route('/api')
# def api_get_news_detail():
#     result = News_Detail.select_all_news()
#     print(request)
#     return result

# 接口名在header中
@app.route('/api')
def api_get_data():
    methods = request.args.get("mt")

    app.logger.debug("mt "+methods)
    if methods:
        from app import api_handle
        return api_handle.handle_api(methods,args=request.args,form=request.form,data=request.data,request=request)
    return toJson(exception_model())
# 文件传参
arg = sys.argv

# for param in arg:
#     if param == "insert":
#        insert("hellotite","this is text")
#     elif param == "show":
#         select(None)
#         pass

def start():
    app.run('0.0.0.0')
    pass


if __name__ == '__main__':

    app.run('0.0.0.0')
