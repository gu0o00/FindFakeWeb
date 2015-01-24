__author__ = 'guojian'
# coding:utf-8
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
def GetLinks(page,url):
    urlp = urlparse(url)
    html = BeautifulSoup(page)
    allLink = html.findAll('a')
    l = urlp.netloc.split('.')
    l.pop(0)
    loc_net = '.'.join(l)
    res = []
    for alink in allLink:
        try:
            alink = str(alink.get('href').encode('utf-8'))
            if loc_net not in alink and 'http:' in alink:
                res.append(alink)
        except :
            print '有异常'
            pass
    return  res