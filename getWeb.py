__author__ = 'guojian'
#coding=utf-8
import urllib2,socket
from BeautifulSoup import BeautifulSoup
def DownloadWeb(url):
    socket.setdefaulttimeout(5)
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
        print "page info is: ",page
        for i in range(5):
            print
        print "after paser is: ",BeautifulSoup(page)
        localfile = open('/home/guojian/webhtml','w')
        localfile.write(page)
        localfile.close()
    except urllib2.HTTPError, e:
        print "Error Code:",e.code
    except urllib2.URLError, e:
        print "Error Reason:",e.reason

if __name__ == '__main__':
    #url = 'http://blog.csdn.net/wklken/article/details/7364390'
    url = "http://www.hao123.com/?1420687830"
    DownloadWeb(url)