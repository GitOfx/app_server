'''
捧腹网
'''
from bs4 import BeautifulSoup

from app.pic_spider import request_url
import asyncio
from app.db.pengfu_db import PengfuJoke
# 捧腹网趣图页 有分页
host = "https://www.pengfu.com/qutu_1.html"
qutu_host = "https://www.pengfu.com/qutu_%s.html"
html_parser = "html.parser"

async def start():
    html = await request_url.request(host, fr="捧腹网趣图页")
    if html != None:
        await parseHtml_getPageNum(html)
    pass


async def parseHtml_getPageNum(html):
    soup = BeautifulSoup(html, html_parser)
    page_num_tag = soup.find("a", class_="page-a page-04")
    page_num = int(page_num_tag.get_text())

    for i in range(page_num):
        url = qutu_host % i
        html = await request_url.request(url, fr="page %s"%i)
        if html != None:
            await parseHtml_getList(html)
        pass

#we only need the title and img in every item
async def parseHtml_getList(html):
    soup = BeautifulSoup(html, html_parser)
    items = soup.find_all('div',class_='list-item bg1 b1 boxshadow')
    for item_div in items:
        title_h = item_div.find('h1',class_='dp-b')
        id = item_div['id']
        a_tag = title_h.find('a')
        href = a_tag['href']
        title = a_tag.get_text()
        img_tag = item_div.find('div',class_='content-img clearfix pt10 relative').find('img')
        img_src = img_tag['src']
        PengfuJoke.AddJoke(id,title,href,img_src)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()