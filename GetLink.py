__author__ = 'guojian'
# coding:utf-8
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import string
def GetLinks(page):
    html = BeautifulSoup(page)
    allLink = html.findAll('a')
    res = []
    for alink in allLink:
        try:
            if alink.get('href') is not None:
                link = unicode(alink.get('href')).encode('utf8')
                if link.startswith('http'):
                    res.append(link)
        except Exception,e:
            print '有异常',e
            pass
        except UnicodeEncodeError,e:
            print alink,'是假链接'
            pass
    return  res
