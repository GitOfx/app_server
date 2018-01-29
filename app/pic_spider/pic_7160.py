'''
多进程抓取图片 把所有的请求 文件 放到队列中
主页中的分类 分类中的页数  每一页的人物  人物多张
先爬到地址

'''
from multiprocessing import Process, Queue
from multiprocessing import Pool
from bs4 import BeautifulSoup
from app.pic_spider import request_url,save_pic
import asyncio

host = 'http://www.7160.com'

request_quen = Queue()

# global total_find
total_find = 0

async def start():
    html =await request_url.request(host, decode=False,fr="index")
    if html != None:
        await prase_index(html)


# 主页 分类地址
async def prase_index(html):
    # print(html)
    soup = BeautifulSoup(html, "html.parser")


    tags = soup.find("div", class_="nav")
    li_list = tags.find_all('li')
    for li in li_list:
        a = li.find('a')
        url = host + a['href']
        title = a.get_text()
        print(title)
        cat_html = await request_url.request(url, fr='分类')
        if cat_html != None:
            await prase_cat(cat_html, url)

# 分类中拿分页列表
async def prase_cat(html, first_url):
    soup = BeautifulSoup(html, "html.parser")
    page_div = soup.find('div', class_='page')

    # 首页直接拿数据
    if page_div == None:
        return

    index = first_url.rindex('/')
    url = first_url[:index+1]
    a_li = page_div.find_all('a')
    for a in a_li:
        if not a.has_attr('href'):
            continue
        href = a['href']
        if href == None:
            continue
        cat_page_html = await request_url.request(url+href,fr="分类2")
        if cat_page_html != None:
            await prase_page(html)


async def prase_page(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find('div','news_bom-left')
    li_list = tag.find_all('li')
    for li in li_list:
        a = li.find('a')
        img_url = host+a['href']
        title = a['title']
        pic_group_html = await request_url.request(img_url,fr="组图")
        if pic_group_html != None:
           await prase_group_nav(pic_group_html,img_url)


async def prase_group_nav(html,page_url):
    soup = BeautifulSoup(html, "html.parser")


    navi_div = soup.find('div',class_ = 'itempage')
    a_list = navi_div.find_all('a')
    index = page_url.rindex("/")
    url = page_url[:index+1]

    for a in a_list:
        try:
            num = int(a.get_text())
            href =url+ a['href']
            if num == 1:
                href = page_url
            img_page_html = await request_url.request(href,decode=False,fr="图片")
            if img_page_html != None:
               await prase_pic(img_page_html)
        except BaseException as e:
            print(e.__repr__())
            continue

async def prase_pic(html):
    soup = BeautifulSoup(html, "html.parser")
    first_img_div = soup.find('div', class_='picsbox picsboxcenter')
    img_tag = first_img_div.find('img')
    first_img_url = img_tag['src']
    title = img_tag['alt']
    global total_find
    total_find += 1
    # print("img url %s"+first_img_url+title % total_find)
    #
    print('找到新图 %s '% total_find)
    await save_pic.save_img(first_img_url,title)
    pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(start())
    loop.close()