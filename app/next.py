
from app import logs
def consumer():
    r = ''
    while True:
        print('r  %s...' % r)
        n = yield r
        print('nyield  %s...%s' % (n,r))
        if not n:
            print('n in if %s...' % n)
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

# c = consumer()
# produce(c)

global a
a = 10

def index():
    url  = "/articles/44955.html"#'http://pic.yesky.com/59/73254559.shtml'
    url  = "https://movie.douban.com/subject/26811587/"#'http://pic.yesky.com/59/73254559.shtml'
    url = url[:url.__len__()-1]
    dot_index = url.rindex("/")
    id = url[dot_index+1:]

    num_str = "118732人看过"  # 118732人看过
    lenth = "人看过".__len__()
    num = int(num_str[0:-lenth])
    logs.info("pos   %s "% (num))
    # str = "1/10"
    # num = str.split("/")
    # print(num[0])
    # print(num[1])
    # url_index = url.rindex('.')
    # num_str = "_%s" % num[1]
    # url = url[:url_index]+num_str+url[url_index:]
    # global a
    # a +=1
    # index  = url.rindex("/")
    # print(url[:index+1])
    # print(a)
    # joke = PengfuJoke(1,'content','detail','imgurl')
    # print("pos %s dot %s id %s "% (pos,dot_index,id))
    # from app.db.news_db import News_Model
    # list=News_Model.get_all(2)


if __name__ == '__main__':
    index()