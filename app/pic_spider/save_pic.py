import sqlite3
import os,time
import asyncio
from app.pic_spider.request_url import request

dbName = 'spide_pic_db'
img_table_name = 'spide_girls_table'
global total_ok
total_ok = 0

async def save_to_file(url,title):

    data = await request(url,decode=False,fr='save')
    if data == None:
        print('返回数据None ')
        return
    index = url.rindex('/')
    # name = "%s%spic/7160%s%s_%s" % (os.path.curdir,os.path.sep,os.path.sep,time.time(),url[index+1:])
    # name = os.path.curdir + os.path.sep + 'pic' + os.path.sep  +"%s _"+url[index+1:] % (time.time())
    name = ".././spide_pic/7160/%s_%s "%(time.time(),url[index+1:])
    print(name)
    print(os.path.curdir)
    insertimgs(name, title)
    await write_file(data,name,title)


async def write_file(data,name,title):

    with open(name, "wb") as file:

        file.write(data)
        global total_ok
        total_ok = total_ok + 1
        print('保存图片 ok %s %s ' % (total_ok, name))


async def save_img(url,title):
    await save_to_file(url,title)


def insertimgs(url,title):
    sql_img = "create table  if not exists  %s(id integer primary key autoincrement,url string not null, title string)" % img_table_name
    sql = 'insert into %s(title ,url   ) values (?,?)' % img_table_name
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute(sql_img)
    cursor.execute(sql, (title, url))

    result = cursor.rowcount
    cursor.close()
    conn.commit()
    conn.close()
    if result > 0:
        return True
    else:
        return False
