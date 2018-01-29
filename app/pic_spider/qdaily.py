# -*- coding: utf-8 -*-
'''
好奇心日报 新闻资讯
http://www.qdaily.com/
先在首页找到tag 和category 和标题
再按路劲根据时间生成请求
解析出新闻id
'''

# http://www.pythondoc.com/flask-sqlalchemy/index.html

from bs4 import BeautifulSoup
import asyncio, time
from app import logs
from app.pic_spider import request_url

host = "http://www.qdaily.com"
cat_more = "categories/categorymore/"
tags_more = "tags/tagmore/"


# tags 1068  1615
# http://www.qdaily.com/categories/categorymore/18/1504931363.json
# http://www.qdaily.com/tags/tagmore/1068/1502777019.json
#


async def start():
    html = await request_url.request(host, decode=False, fr="index")
    if html != None:
        await prase_index(html)
    pass


async def prase_index(html):
    '''解析出首页的 category and tags'''
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find("div", class_="page-header-ft hidden")
    cates = divs.find_all("li", class_="item cate ");
    for ul in cates:
        a = ul.find('a')
        url = a['href']  # /tags/1068.html  /categories/18.html
        spans = a.find_all('span')
        title = ""
        if len(spans) > 1:
            title = spans[1].get_text()
        logs.info(title + " url " + url)

        type = ""

        if "tags" in url:
            type = "tags"
            pass
        elif "categories" in url:
            type = "categories"
            pass
        pos = url.rindex("/")
        dot_index = url.rindex(".")
        cat_id = url[pos + 1:dot_index]

        await get_more_list(type, cat_id, title)
        html = await request_url.request(host + url, fr="page")
        if html != None:
            await prase_cate_page(html, title, type, cat_id)


async def prase_cate_page(html, title, type, cat_id):
    '''每个种类的第一页 只要 /articles/44955.html'''
    soup = BeautifulSoup(html, "html.parser")
    a_all = soup.find_all("a")
    for a in a_all:
        href = a["href"]
        if "/articles/" in href:
            pos = href.rindex("/")
            dot_index = href.rindex(".")
            artical_id = href[pos + 1:dot_index]
            add_news_cat(type, title, cat_id, artical_id)
            pass


def add_news_cat(type, cate_name, cat_id, artical_id):
    from app.db.news_db import News_Category
    News_Category.add_news_cate(type, cat_id, cate_name, artical_id)
    News_Category.commit_data()
    pass



async def get_more_list(type, cat_id, title,count = 0,time_now = 0):
    '''http://www.qdaily.com/categories/categorymore/4/1504229103.json
        根据id 拉json
    '''
    url = host
    if time_now == 0:
         time_now = round(time.time())
    if type in cat_more:
        url = "%s/categories/categorymore/%s/%s.json" % (host, cat_id, time_now)
    else:
        url = "%s/tags/tagmore/%s/%s.json" % (host, cat_id, time_now)

    logs.info("get json " + url)
    json = await request_url.request(url, decode=True, fr="json")
    # logs.info("json: " + str(json))
    if json is not None:
        from app.data_model import base_model
        data_dict = base_model.toModel(json)
        if "data" in data_dict:
            feeds_list = data_dict["data"]
            if feeds_list is not None:
                for feed_dict in feeds_list:
                    if "post" in feed_dict:
                        post = feed_dict["post"]
                        if "id" in post:
                            artical_id = post["id"]
                            add_news_cat(type, title, cat_id, artical_id)
                            pass
                        pass
                pass

        pass
    # count += 1
    # if count < 10:
    #     time.sleep(5)
    #     time_now = round(time.time())
    #     logs.info("catid %s count %s time %s"%(cat_id,count,time_now))
    #     await get_more_list(type, cat_id, title, count,time_now)


async def request_detail_all():
    '''从数据库中取出id  1504769093  1504566943  1504253733
        拼成url http://www.qdaily.com/articles/43262.html
      拼凑
    '''
    from app.db.news_db import News_Category
    all_new = News_Category.get_all()
    cout = 0
    if all_new is not None:
        for news in all_new:
            artical_id = news.artical_id
            url = "%s/articles/%s.html" % (host, artical_id)
            logs.info(url)
            cout += 1
            resp_html = await request_url.request(url, decode=False, fr="detail page")
            if resp_html is not None:
                try:
                    prase_detail_news(resp_html, artical_id)
                    pass
                except BaseException as e:
                    logs.error("prase_detail_news %s" % ( e.__repr__()))


            pass
    logs.info("total %s " % cout)
    pass


def prase_detail_news(html, artical_id):
    '''具体每一页的新闻'''
    from app.db.news_db import News_Model, News_Img

    soup = BeautifulSoup(html, "html.parser")
    div_main = soup.find("div", class_="main")
    article_detail_hd = div_main.find("div", class_="article-detail-hd")

    head_img = article_detail_hd.find("img")
    title = "" if head_img == None else head_img['alt']
    img_src = "" if head_img == None else head_img['data-src']

    article_detail_bd = div_main.find("div", class_="article-detail-bd")
    time = article_detail_bd.find("span", class_="date smart-date")["data-origindate"]
    excerpt = article_detail_bd.find("p", class_="excerpt").get_text()
    detail_div = article_detail_bd.find("div", class_="detail")

    News_Model.add_news_detail(artical_id=artical_id, title=title, time=time, excerpt=excerpt,
                               content=detail_div.get_text(),

                               html=detail_div.prettify())

    News_Img.add_news_img(artical_id, img_src, title)
    imgs = detail_div.find_all("div", class_="com-insert-images")

    for img in imgs:
        img_url = img.find('img')["data-src"]
        desc = img.find('p')

        des = "" if desc == None else desc.get_text()
        News_Img.add_news_img(artical_id, img_url,des )

    # logs.info("html "+detail_div.prettify())



async def reauest_id():
    artical_id = "44965"
    url = "%s/articles/%s.html" % (host, artical_id)
    logs.info(url)

    resp_html = await request_url.request(url, decode=False, fr="detail page")
    if resp_html is not None:
        prase_detail_news(resp_html, artical_id)
    pass


def refresh_news():
    # RuntimeError: Event loop is closed
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
    tasks = [start(), request_detail_all()]
    loop.run_until_complete(asyncio.wait(tasks))
    # loop.run_until_complete(get_more_list("categorymore",54,"test"))
    # loop.run_until_complete(start())

    # loop.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [start(),request_detail_all()]
    loop.run_until_complete(asyncio.wait(tasks))
    # loop.run_until_complete(get_more_list("categorymore",54,"test"))
    # loop.run_until_complete(start())
    loop.close()
