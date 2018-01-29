'''
内涵段子社区 图片
'''
from bs4 import BeautifulSoup

from app.pic_spider import request_url
import asyncio

host = "http://neihanshequ.com/pic/"

async def start():
    html = await request_url.request(host, fr="内涵段子主页")
    if html != None:
        await parseHtml(html)
    pass

async def parseHtml(html):
    soup = BeautifulSoup(html, "html.parser")
    detail_list_tag = soup.find("ul", id="detail-list")
    li_tags = detail_list_tag.find_all("li")
    for li_tag in li_tags:
        img = li_tag.find("img")
        print(li_tag)
        print(img)
        text = li_tag.string
        print(text)
        pic = img['src']
        print("%s %s "%(text,pic))
    pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()