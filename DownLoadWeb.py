__author__ = 'guojian'
#coding=utf-8
import urllib2,socket
from BeautifulSoup import BeautifulSoup
def UseProxy():
    import socks,socket
    enable_proxy = True
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',7070)
    socket.socket = socks.socksocket
def NoProxy():
    enable_proxy = False
def DownloadWeb(url,enable_proxy = False):
    if enable_proxy :
        UseProxy()
    socket.setdefaulttimeout(8)
    #可以加入参数（无参数使用get，以下方式使用post）
    #params = {"wd":"a","b":"2"}
    #加入请求头信息，以便识别
    i_headers = {"User-Agent":"Mozilla/5.0 (windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Accept":"text/plain"}
    #use post,have some params post to server,if not support ,will throw exception
    #req = urllib2.Request(url, data=urllib.urlencode(params), headers=i_headers)
    req = urllib2.Request(url, headers=i_headers)
    #创建request后，还可以进行其他添加,若是key重复，后者生效
    #request.add_header('Accept','application/json')
    #可以指定提交方式
    #request.get_method = lambda: 'PUT'
    try:
        page = urllib2.urlopen(req).read()
        assert isinstance (page,str )
        return page
    except urllib2.HTTPError, e:
        print 'this url is :' ,url
        print "Error Code:",e.code
        return None
    except urllib2.URLError, e:
        print "Error Reason:",e.reason
        return None
    except Exception,e:
        print e
        return None


if __name__ == '__main__':
    #url = 'http://riching.iteye.com/blog/1968769'
    #url = "http://www.hao123.com"
    url = 'http://www.sotrip.com/overchina/jycy.php'
    print DownloadWeb(url)