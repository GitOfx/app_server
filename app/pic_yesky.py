import urllib3
from bs4 import BeautifulSoup
import sqlite3
from app.db.user_db import Table_user ,dbName
import time, threading
import os
import asyncio
import logging

host = "http://pic.yesky.com"

global total_img
global total_fail
global total_ok

total_img = 0
total_fail =0
total_ok = 0

img_table_name = "girl_yesky_table"

async def request(url,decode=True,fr=None):
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
    print("请求出错 "+str(response.status))

girl_cat = "美女图片"

# 主页只要找到入口
async def parase_index(html,catgory = "no cat"):
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("ul", class_="nav_left")
    li_list = tags.find_all('li')
    for li in li_list:
        url = li.find("a")['href']
        cat = li.find('a').get_text()
        print(cat)
        if cat == girl_cat:
            girl_html = await request(url,fr = "列表")
            if girl_html != None:
                await prase_list(girl_html)

async def prase_list(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("div", class_="lb_box")
    navi = tags.find('div',class_ = 'flym')
    a_list = navi.find_all('a')
    for a in a_list:
        url = host+a['href']
        page = a.get_text()
        show_html = await request(url,fr="展示")
        if show_html != None:
            await prase_show(show_html)

async def prase_show(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("div", class_="lb_box")
    dl_list = tags.find_all('dl')
    for dl in dl_list:
        dd = dl.find('dd')
        a = dd.find('a')
        detail_url = a['href']
        title = a['title']
        show_html_list = await request(detail_url, fr="展示列表")
        if show_html_list != None:
            await prase_detail_list(show_html_list)


async def prase_detail_list(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("div",id = 'scroll', class_="effect_scroll")
    li = tags.find('li')
    a = li.find('a')
    url = a['href']
    span = li.find('span')
    num_str = span.get_text() #1/10
    num = num_str.split("/")[1]
    url_index = url.rindex('.')
    for i in range(1,int(num)):
        url_str = url
        if i!= 1:
            num_str = "_%s" % i
            url_str = url[:url_index] + num_str + url[url_index:]

        girl_detail_html = await request(url_str,fr="图片页")
        if girl_detail_html != None:
            await prase_gitl_detail(girl_detail_html)

async def prase_gitl_detail(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("div",  class_="l_effect_img_mid")
    img = tags.find('img')
    img_url = img['src']
    title = img['alt']
    await save_img(img_url,title)


async def save_to_file(url,title):

    data = await request(url,decode=False,fr='save')
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


async def write_file(data,name,title):

    with open(name, "wb") as file:
        insertimgs(name,title)
        file.write(data)


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

async def start():
    html =await request(host, fr="index")
    if html != None:
        await parase_index(html)

if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    loop.run_until_complete(start())
    loop.close()