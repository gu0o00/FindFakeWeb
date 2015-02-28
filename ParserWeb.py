__author__ = 'guojian'
# coding:utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
from DownLoadWeb import DownloadWeb
import re

class ParserWeb:
    '单纯的对一个url页面进行分析'
    def __init__(self,url,enable_proxy = False):
        self.url = url
        self.url_parse = urlparse(url)
        self.page = None
        self.enable_proxy = enable_proxy
        pass
    def isIP(self):
        '判断url中是否包含IP'
        re_ip = "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})){3}"
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
        if page == None:
            return "该网站暂无备案"
        html = BeautifulSoup(page)
        info = html.findAll('td',attrs={'class':'tdright'})
        if len(info) > 1:
            return info[2].text
        else:
            return "该网站暂无备案"
    def parserLink(self):
        '分析网站的链接对象，统计出指向本站链接和外站链接的个数'
        allLink = []
        if self.page is None:
            self.page = DownloadWeb(self.url,self.enable_proxy)
        in_count = 0
        out_count = 0
        if self.page is not None:
            self.html = BeautifulSoup(self.page)
            allLink = html.findAll('a')
            l = self.url_parse.netloc.split('.')
            l.pop(0)
            loc_net = '.'.join(l)
            try:
                for alink in allLink:
                    if alink is None or alink.get('href') is None:
                        continue
                    alink = str(alink.get('href').encode('utf-8'))
                    if loc_net not in alink and 'http:' in alink:
                        out_count += 1
                        #print alink
                    else:
                        in_count += 1
                        #print alink
            except AttributeError,e:
                print e,alink
        res = [len(allLink),in_count,out_count]
        return res
    def urlAge(self):
        '判断域名注册年龄'
        seourl = 'http://seo.chinaz.com/?host='
        target = self.url.replace(':','%3a').replace('/','%2f')
        page = DownloadWeb(seourl + target)
        if page == None:
            return '注册时间无法获取'
        html = BeautifulSoup(page)
        info = html.findAll('font',attrs={'color':'blue'})
        if len(info) > 1:
            return info[3].text
        else:
            return '注册时间无法获取'
    def urlLen(self):
        return len(self.url)
    def FormCount(self):
        formList = self.html.findAll('form')
        return len(formList)
    def ImgCount(self):
        imgList = self.html.findAll('img')
        return len(imgList)
    def comParser(self):
        resList = [self.url]
        resList.append(self.isIP())
        resList.append(self.underlineCount())
        resList.append(self.isCopyright())
        resList.append(self.parserLink())
        resList.append(self.urlAge())
        resList.append(self.urlLen())
        resList.append(self.FormCount())
        resList.append(self.ImgCount())
        return resList
    
if __name__ == '__main__':
    url = 'http://www.21fj.com/'
    print url
    pw = ParserWeb(url)
    print pw.isIP()
    print pw.underlineCount()
    print pw.isCopyright()
    print '网站的链接个数:',pw.parserLink()
    print pw.urlAge()
    print pw.urlLen()
    print pw.FormCount()
    print pw.ImgCount()
