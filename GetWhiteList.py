__author__ = 'guojian'

#coding=utf-8

import urllib2,re,os,sys
from BeautifulSoup import BeautifulSoup
from DownLoadWeb import DownloadWeb
import string
sys.path.append('libsvm')
sys.path.append('libsvm/python')
from svmutil import *

def getUrl(startUrl):
    print startUrl
    linklist = []
    middlelist = []

    page = DownloadWeb(startUrl)
    assert isinstance (page,str )
    html = BeautifulSoup(page)
    for link in html.findAll('a'):
        link = unicode(link.get('href')).encode('utf8')
        if link.startswith('http'):
            linklist.append(link)
            #print alink
        else:
            middlelist.append(link)
    #http://www.sina.com.cn/ddt/wangzhi/index.html
    #to
    #http://www.sina.com.cn/ddt/wangzhi
    url = '/'.join(startUrl.split('/')[:-1])
    for elink in middlelist:
        aurl = url + '/' + elink
        print aurl
        page = DownloadWeb(aurl)
        assert isinstance (page,str )
        html = BeautifulSoup(page)
        for link in html.findAll('a'):
            link = unicode(link.get('href').encode('utf8'))
            linklist.append(link)
    print len(linklist)
    return linklist

if __name__ == '__main__':
    #url_white = 'http://site.baidu.cn'
    url_white = 'http://www.sina.com.cn/ddt/wangzhi/index.html'
    localfile = "List/WhiteList.txt"
    whiteList = getUrl(url_white)
    whiteFile = open(localfile,'w')
    for item in whiteList:
        whiteFile.write(item + os.linesep)
    whiteFile.close()

