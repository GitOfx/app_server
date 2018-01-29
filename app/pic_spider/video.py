from multiprocessing import Process, Queue
from multiprocessing import Pool
from bs4 import BeautifulSoup
from app.pic_spider import request_url,save_pic
import asyncio
import urllib3
import os,time

from selenium import webdriver
# https://seleniumhq.github.io/selenium/docs/api/py/index.html
host = 'http://91.91p10.space/v.php?next=watch'
# host = 'http://93.91p12.space/v.php?category=long&viewtype=basic'

request_quen = Queue()


async def start():
    html =await request_url.request(host,decode=False, fr="index")
    # brower = webdriver.Chrome();
    # brower.get(host)
    # time.sleep(3);
    # html = brower.page_source;
    if html != None:
        await prase_index(html)

async def prase_index(html):
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all("div", class_="listchannel")
    for div in tags:
        a = div.find('a')
        url = a['href']
        title = a.find('img')['title']
        print(title+" url "+url)
        html = await request_url.request(url, fr="page")
        if html != None:
            await prase_page(html)

async def prase_page(html):
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find("video", id="vid_html5_api")
    if tags != None:
        # print("no video")
        source = tags.find('source')
        url = source['src']
        print("video " + url)
        await request_url.download(url)
        return

    tags = soup.find("textarea", id="fm-video_link")
    if tags == None:
        print("no video")
        return
    # source = tags.find('source')
    url = tags.get_text()
    print("video "+url)

    # await request_url.download(url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(start())
    loop.close()