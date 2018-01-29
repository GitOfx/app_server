# -*- coding: utf-8 -*-
# http://www.jianshu.com/p/b036e6e97c18    object HTTPResponse can't be used in 'await' expression
import urllib3
from bs4 import BeautifulSoup
import sqlite3
from app.db.user_db import Table_user ,dbName
import time, threading
import os
import asyncio
import logging

host = "http://74xk.com"

global total_img
global total_fail
global total_ok

total_img = 0
total_fail =0
total_ok = 0
async def request_page(url):
    html = await request(url,True)
    if html != None:
        await praseRsp(html)

page_url = []

async def praseRsp(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("div", class_="box list channel")
    lis_tag = tags.find_all('li')
    page_tag = tags.find('div',class_ = 'pagination')
    a_tags = page_tag.find_all('a');

    if page_url :
        for a in a_tags:
            url = a['href']
            page_url.append(url)
            if url.index("html") >0:
                logging.debug("页面里的链接 马上请求 "+host+url)
                request_page(host+url)



    for tag in lis_tag:
        url = host+tag.find('a')['href']

        title = tag.find('a').get_text()


        img_html = await request(url,True,fr="list")
        img_soup = BeautifulSoup(img_html, "html.parser")
        # page_url = img_soup.findAll('div',class_='post')
        imgs = img_soup.find_all('img')
        for img_tag in imgs:
            img_url = img_tag['src']
            # print("find "+img_url)
            await save_img(img_url,title)

img_table_name = 'girl_img_table'


async def request(url,decode=False,fr=None):
    http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1.0, read=5.0),retries=False)
    print(fr+' request: '+url)
    logging.debug(fr+' request: '+url)
    try:
        response =  http.request("GET", url,redirect=False)
    except BaseException as e:
        global total_fail
        total_fail += 1
        print("请求出错 %s %s" %(total_fail,e.__repr__()))

        return
    if response == None:
        print("请求回来 结果为None " )
        return
    if response.status == 200:
         if decode:
             return response.data.decode("GBK")
         return response.data
    print("请求出错 "+response.status)

async def write_file(data,name,title):

    with open(name, "wb") as file:
        insertimgs(name,title)
        file.write(data)

async def save_to_file(url,title):

    data = await request(url,fr='save')
    if data == None:
        print('返回数据None ')
        return
    index = url.rindex('/')
    name = "%s%spic%s%s_%s" % (os.path.curdir,os.path.sep,os.path.sep,time.time(),url[index+1:])
    # name = os.path.curdir + os.path.sep + 'pic' + os.path.sep  +"%s _"+url[index+1:] % (time.time())

    global total_ok
    total_ok = total_ok+1
    print('保存图片 ok %s %s ' % (total_ok, name))

    await write_file(data,name,title)



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

def selectImgs(count):
    sql = 'select * from  %s  order by id limit 0,%s' % (img_table_name,count)
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    imgs = []
    for img in result:
        print(img)
        imgs.append(img[1])
    return imgs

#每一个主页
async def task_category(url):

    html = await request(url,True,fr='categoty')

    if html != None:
        await prase_category_html(html)

async def prase_detail_html(html,title):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("div", class_="post")
    img_list = tags.find_all('img')
    global  total_img
    for img in img_list:
        img_url = img['src']
        total_img = total_img+1
        print("新加图片 total %s" % total_img)
        await save_img(img_url,title)


async def prase_category_html(html,page = 0):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("div", class_="box list channel")
    lis_tag = tags.find_all('li')

    # a_tags = lis_tag.findAll('a');
    for img_url_tag in lis_tag:
        img_url = host+img_url_tag.find('a')['href']
        title = img_url_tag.find('a').get_text()
        detail_html = await request(img_url,fr='detail')
        if detail_html != None:
            await prase_detail_html(detail_html,title)

    page_tag = tags.find('div', class_='pagination')
    if page == 1:
        return
    a_list_tag = page_tag.find_all("a")
    for a in a_list_tag:
        new_page_url = host+a['href']
        try:
            if new_page_url.index("html") > 0:
                print("goto new page " + new_page_url)
                await task_category(new_page_url, 1)
        except BaseException as e:
            print(e.__repr__())
            return



if __name__ == '__main__':
    pages = ["11","12","13","14","15","16","17","18"]
    # pages = ["12","13"]

    task = []
    for page in pages:
        url =  host + "/pic/%s/" % page
        task.append(task_category(url))

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(*task))
    loop.close()