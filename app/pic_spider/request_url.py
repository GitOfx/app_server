import urllib3
global total_fail
import os,time
import urllib.request
import sys
import random
from app.api_handle import toModel
from app import logs

total_img = 0
total_fail =0
total_ok = 0

def report(count, blockSize, totalSize):
  percent = int(count*blockSize*100/totalSize)
  sys.stdout.write("\r%d%%" % percent + ' complete')
  sys.stdout.flush()

def getIp():
    http = urllib3.PoolManager(retries=True)
    resp = http.request("GET","http://127.0.0.1:8000/?types=0&count=50&country=%E5%9B%BD%E5%86%85")
    re = toModel()
    return re[0]

async def download(url):
    # http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1.0, read=5.0), retries=False)
    #
    # f = http.urlopen(url)
    index = url.rindex('/')
    name = ".././spide_pic/video/%s_%s " % (time.time(), url[index + 1:])
    f = urllib.request.urlretrieve(url,name,reporthook= report)
    # with open(name, "wb") as code:
    #     code.write(f.read())


async def request(url,decode=True,fr=None):
    '''由url 返回网页html 默认解压编码 '''
    # timeout=urllib3.Timeout(connect=1.0, read=5.0),
    http = urllib3.PoolManager(retries=True)
    logs.info(fr + ' request: ' + url)
    # ip = getIp()  代理的时候用到的
    try:
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
        ]

        HEADER = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            "Cache-Control": "max-age=0",
            'Accept-Encoding': 'gzip, deflate',
        }
        time_now = round(time.time())
        # proxy = urllib3.ProxyManager('http://localhost:3128/')
        proxy_add = "http://60.21.206.165:9999/";
        header = {"Accept-Language":"zh-CN,zh;q=0.8",
                                                     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                                     "Accept-Encoding":"gzip, deflate, sdch",
                                                     "Cache-Control":"max-age=0",
                                                     "Proxy-Connection":"keep-alive",
                                                     "Upgrade-Insecure-Requests":"1",
                                                     "Host":"91.91p10.space",
                                                      'User-Agent': random.choice(USER_AGENTS)
                                                     }
        # proxy = urllib3.ProxyManager(proxy_add
        #                              ,proxy_headers=header)
        # cokie="__cfduid=dc5a68c83093862f2a46ec7b64391a94a1500209152; CLIPSHARE=d6lu482sqh8mbkrgdk4r87nd36; show_msg=1; watch_times=1; __utma=186402657.410295313.%s.%s.1500212219.2; __utmb=186402657.0.10.1500212219; __utmc=186402657; __utmz=186402657.%s.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); AJSTAT_ok_pages=12; AJSTAT_ok_times=1; __dtsu=2DE7B66B03606B5924437DB102BD85DB"%(time_now,time_now,time_now);

        response =  http.request("GET", url,headers=HEADER,
                                 redirect=False)
    except BaseException as e:
        global total_fail
        total_fail += 1
        logs.error("请求出错 %s %s" % (total_fail, e.__repr__()))

        return
    if response == None:
        logs.error("请求回来 结果为None ")
        return
    if response.status == 200:
         if decode:
             return response.data.decode("utf-8")
         return response.data
    logs.error("请求出错 " + str(response.status))

# if __name__ == '__main__':
    # ip = getIp()


