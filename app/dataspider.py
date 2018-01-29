# -*- coding: utf-8 -*-
# https://urllib3.readthedocs.io/en/latest/user-guide.html
# https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

import urllib3
from bs4 import BeautifulSoup
from app.db.news_db import News,News_Detail
import asyncio

host = "http://www.qdaily.com/"
def getHtml(url):
    http = urllib3.PoolManager()
    print(url)
    response =  http.request("GET",url)
    print(response.status)


    src = response.data.decode("utf-8")


    return src

def praseHtml(html):
    soup = BeautifulSoup(html,"html.parser")
    tags = soup.find_all("div", class_="packery-item")
    for tag in tags:
        atag = tag.a
        url = host+atag["href"]
        imgtags = tag.find(class_="pic imgcover").find('img')

        imgurl = imgtags['data-src']

        # titletag = tag.find(class_='smart-dotdotdot')
        # print(titletag)
        title = imgtags['alt']

        timetag= tag.find(class_='smart-date')
        # print(timetag)
        time = timetag['data-origindate']

        categorytag = tag.findAll('span')[1]
        # print(categorytag)
        category = categorytag.string
        news = News(title,time,category,imgurl,url)
        news.save_db()
        # print("title: %s time: %s ctegory %s url:%s img:%s" % (title,time,category,url,imgurl))

def getNewsDetail():
    news_list = News.selectAllNews()
    tasks = []
    for news_item in news_list:
        request_task(news_item)

    # loop = asyncio.get_event_loop()
    #
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    pass

def request_task(news_item):
    src = getHtml(news_item.url)
    praseNewsDetail(src)

def praseNewsDetail(html):
    soup = BeautifulSoup(html, "html.parser")
    maintag = soup.find('div',class_ = 'main')
    if maintag == None:
        return
    titletag = maintag.find('div',class_='article-detail-hd')
    title_img_tag = titletag.find('img')
    title_img_url = title_img_tag['data-src']
    title_tag = titletag.find(class_='title')
    title_text = title_tag.string
    category_tag = titletag.find(class_='category-title')
    category_text = category_tag.find_all('span')[1].string

    author_tag = maintag.find('div',class_='author-share clearfix')
    author_name = author_tag.find('span',class_ = 'name').string
    time = author_tag.find('span',class_= 'date smart-date')['data-origindate']

    content_tag = maintag.find('div',class_='article-detail-bd')
    if content_tag == None:
        return
    excerpt = content_tag.find(class_ = 'excerpt').string

    detail_tag = content_tag.find('div',class_ = 'detail')

    detail_p_tags = detail_tag.find_all('p')
    detail_img_tags = detail_tag.find_all('img')
    content_txt = ' '
    for p in detail_p_tags:
        if  p.string != None:
            if content_txt:
                content_txt = p.string
            else:
                print("ppppp" + p.string + " " + content_txt)
                content_txt += p.sting



    img_list = []
    for img in detail_img_tags:
        imgurl = img['data-src']
        img_list.append(imgurl)


    news_detail = News_Detail(title_text,category_text,excerpt,time,content_txt,img_list,content_tag.get_text())
    news_detail.save()

def re_task(url):
    src = getHtml(url)
    praseHtml(src)

if __name__ == '__main__':
    url = "http://www.qdaily.com/"
    # loop = asyncio.get_event_loop()
    #
    # loop.run_until_complete(asyncio.wait(re_task(url)))
    # loop.close()
    re_task(url)
    getNewsDetail()