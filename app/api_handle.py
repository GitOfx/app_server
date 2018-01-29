'''
通过方法请求名处理 做请求 然后返回，接口名可已有多个是个列表
'''

from app.data_model.base_model import Base_Model,toJson,toModel
from app.main import log

import os

def handle_api(api_names,args = None,form=None,data = None,request = None):
    ip = request.remote_addr
    log.info("ip "+ip)
    json_data = None
    if api_names == "get_news_list":
        json_data = handle_get_news_list()

    if api_names == "get_pic":
        json_data = handle_pic()

    if api_names == "get_duanzi":
        page_size = args.get('page_size')
        page_num = args.get('page_num')
        json_data = hanle_api_pengfu(page_size,page_num)

    if api_names == "refresh_news":
        from app.pic_spider import qdaily
        qdaily.refresh_news()
        json_data = "refresh ok"

    if api_names == "create_db":
        from app.db import news_db
        news_db.create_db()
        json_data = "create ok"

    if api_names == "get_news_cat":
        from app.db import news_db
        result_list = news_db.News_Category.get_all(2)
        json_data = toJson(result_list)

    if api_names == "get_news_model":
        from app.db import news_db
        result_list = news_db.News_Model.get_all(2)
        json_data = toJson(result_list)
    # from app.data_model.base_model import base_model
    # log.info("data " + str(json_data))

    base_model = Base_Model("success",0,json_data)

    json = toJson(base_model)
    log.info("result: " + json)
    return json


def hanle_api_pengfu(page_size = 0,page_num = 0):
    from app.db.pengfu_db import PengfuJoke
    joke_list = PengfuJoke.GetPage(page_size,page_num)
    json = toJson(joke_list)
    from app.main import app
    print("result: " + json)
    return json

def handle_get_news_list(limit = 5):
    from app.db.news_db import News_Model,News_Img
    news_list = News_Model.get_all(limit=limit)
    datajson = toJson(news_list)
    return datajson
    pass


def handle_pic():
    dir = "static/pic"
    num = 0
    dir_path = "static/pic"
    pic_list = []
    for pic in os.listdir(dir):
        num +=1
        pic_dir = "%s/%s" % (dir_path,pic)
        # print(pic_dir)
        pic_list.append(pic_dir)
        if num >200:
            break

    json = toJson(pic_list)
    from app.main import app
    print("result: " + json)
    return json

def testAPI(api_names):
    if api_names == "get_news_cat":
        from app.db import news_db
        result_list = news_db.News_Category.get_all(2)
        # json_data = toJson(result_list)
    if api_names == "get_news_model":
        from app.db import news_db
        result_list = news_db.News_Model.get_all(10)
        # json_data = toJson(result_list)

    base_model = Base_Model("success", 0, data=result_list)

    json = toJson(base_model)
    log.info("result: " + json)

if __name__ == '__main__':
    # hanle_api_pengfu(5,1)
    # handle_pic()
    testAPI("get_news_model")