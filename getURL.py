__author__ = 'guojian'

#coding=utf-8

import urllib2,re,os
from BeautifulSoup import BeautifulSoup

def getUrl(startUrl,filename):
    html = urllib2.urlopen(url).read()
    html = str(BeautifulSoup(html))
    #print html

    myfile = open(filename,'w')
    re_find = re.compile('.+?href=\"(http.+?)\"')
    reslist = re_find.findall(html)
    for item in reslist:
        myfile.write(item + os.linesep)
    myfile.close()

if __name__ == '__main__':
    os.pardir
    url = 'http://site.baidu.com/'
    localfile = "List/WhiteList.txt"
    getUrl(url,localfile)
