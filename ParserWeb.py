__author__ = 'guojian'
# coding:utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
from DownLoadWeb import DownloadWeb
import re

class ParserWeb:
    def __init__(self,url):
        self.url = url
        self.url_parse = urlparse(url)
        pass
    def isIP(self):
        '判断url中是否包含IP'
        re_ip = "^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})){3}$"
        re_match = re.compile(re_ip)
        res = re_match.match(self.url_parse.netloc)
        if res:
            return True
        else:
            return False
    def underlineCount(self):
        '返回域名中下划线的个数'
        return self.url.count('_')
    def isCopyright(self):
        '判断改网站是否有备案'
        seourl = 'http://tool.chinaz.com/beian.aspx?s='
        target = seourl+ self.url_parse.netloc
        page = DownloadWeb(target)
        html = BeautifulSoup(page)
        info = html.findAll('td',attrs={'class':'tdright'})
        if len(info) > 1:
            return info[2].text
        else:
            return "该网站暂无备案"
    def parserLink(self):
        '分析网站的链接对象，统计出指向本站链接和外站链接的个数'
        allLink = []
        page = DownloadWeb(self.url)
        in_count = 0
        out_count = 0
        if page != None:
            html = BeautifulSoup(page)
            allLink = html.findAll('a')
            l = self.url_parse.netloc.split('.')
            l.pop(0)
            loc_net = '.'.join(l)
            print loc_net
            for alink in allLink:
                alink = alink.get('href')
                if loc_net not in str(alink) and 'http:' in str(alink):
                    out_count += 1
                    #print alink
                else:
                    in_count += 1
                    #print alink
        res = [len(allLink),in_count,out_count]
        return res

if __name__ == '__main__':
    url = 'http://ent.sina.com.cn/download/'
    pw = ParserWeb(url)
    #print pw.isIP()
    #print pw.underlineCount()
    #print pw.isCopyright()
    print '网站的链接个数:',pw.parserLink()