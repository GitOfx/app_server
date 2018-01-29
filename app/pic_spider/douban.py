'''
抓取豆瓣电影数据 影评
https://movie.douban.com/chart  排行榜
'''

import asyncio

from bs4 import BeautifulSoup

from request_url import request
from app.main import log

host = "https://movie.douban.com"
host_chart = "https://movie.douban.com/chart"

async def request_index():
    '''先分析首页  豆瓣新片榜  再拿旁边的 分类'''
    html = await request(host_chart,decode=False,fr="豆瓣首页")
    if html != None:
        try:
            await prase_index(html)
            pass
        except BaseException as e:
            log.info(e)
            log.info(html)
            pass

    pass

async def prase_index(html):
    '''先分析首页  豆瓣新片榜  再拿旁边的 分类'''
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find("div", class_="indent")
    tables = divs.find_all("table")
    for table in tables:
        # https://movie.douban.com/subject/26811587/
        a = table.find("a")
        url = a["href"]
        url = url[:url.__len__() - 1]
        dot_index = url.rindex("/")
        id = url[dot_index + 1:]
        log.info("movie id %s "%(id))
        # await requestDetail(id)
        await request_comment(id,0)
        pass
    pass

async def requestDetail(id):
    # https://movie.douban.com/subject/26811587/
    url = "%s/subject/%s/" %(host,id)
    html = await request(url, decode=True, fr="电影详情")
    if html != None:
        await parseDetail(html)


async def parseDetail(html):
    # log.info(html)
    soup = BeautifulSoup(html, "html.parser")
    div_article = soup.find("div",class_ = "article")
    div_mainpic = div_article.find("div",class_ = "mainpic")
    # a_more_pic = div_mainpic.find("a")

    # url_more_pic = a_more_pic["href"]
    # url_main_pic = div_mainpic.find("img")["src"]
    #
    # div_info = div_mainpic.find("div",class_ = "info")
    # https://movie.douban.com/subject/26811587/collections
    # https://movie.douban.com/subject/26811587/collections?start=0

    pass

async def request_comment(id,page):
    url = "https://movie.douban.com/subject/%s/collections?start=%s" %(id,page)
    html = await request(url, decode=True, fr="评论 %s"%(page))
    if html != None:
        await parse_comment(html,id)
    if page < 500:
        page = page+20
        await request_comment(id,page)

total_comment = 0
cur_page = 0
async def parse_comment(html,id):
    soup = BeautifulSoup(html, "html.parser")
    div_article = soup.find("div", class_="article")
    num_span = div_article.find("span",id="collections_bar")
    num_str = num_span.get_text() #118732人看过
    lenth = "人看过".__len__()
    num = int(num_str[0:-lenth])
    total_comment = num

    sub_ins = div_article.find("div",class_="sub_ins")
    tables = sub_ins.find_all("table")
    for table in tables:
        p = table.find_all("p")
        for p1 in p:
            p_str = p1.get_text()
            log.info(p_str)
            from app.db.movie_db import Movie_Comment
            comment = Movie_Comment(p_str,id)
            Movie_Comment.add_movie_comment(p_str,id)
            pass

        pass
    pass

async def start():
    await request_index()
    pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [start()]
    loop.run_until_complete(asyncio.wait(tasks))

    loop.close()