__author__ = 'guojian'

#coding=utf-8

import urllib2,re,os,sys
from BeautifulSoup import BeautifulSoup
sys.path.append('libsvm')
sys.path.append('libsvm/python')
from svmutil import *

def getUrl(startUrl):
    print startUrl
    i_headers = {"User-Agent":"Mozilla/5.0 (windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Accept":"text/plain"}
    req = urllib2.Request(startUrl, headers=i_headers)

    try:
        page = urllib2.urlopen(req).read()
        html = str(BeautifulSoup(page))
        re_find = re.compile('.+?href=\"(http.+?)\"')
        reslist = re_find.findall(html)
        print len(reslist)
        return reslist
    except urllib2.HTTPError, e:
        print "Error Code:",e.code
    except urllib2.URLError, e:
        print "Error Reason:",e.reason

if __name__ == '__main__':
    url_white = 'http://hao.360.cn'
    localfile = "List/WhiteList.txt"
    whiteList = getUrl(url_white)
    whiteFile = open(localfile,'w')
    for item in whiteList:
        whiteFile.write(item + os.linesep)
    whiteFile.close()

