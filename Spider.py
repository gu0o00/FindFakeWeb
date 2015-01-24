__author__ = 'guojian'
# coding:utf-8
import ThreadPool
from DownLoadWeb import DownloadWeb
from GetLink import GetLinks
from ParserWeb import ParserWeb
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
from time import sleep
from threading import Thread
from Queue import Queue
class Spider(Thread):
    '生产者，爬取url链接放入队列'
    def __init__(self, t_name, queue, starturl):
        Thread.__init__(self, name = t_name)
        self.urlqueue = queue
        self.starturl = starturl
    def run(self):
        page = DownloadWeb(self.starturl)
        links = GetLinks(page,self.starturl)
        for alink in links:
            self.urlqueue.put(alink)
        urlList = []
        urlList += links
        i = 0
        while len(urlList) > i:
            alink = urlList[i]
            i = i + 1
            print '正在下载:',alink
            page = DownloadWeb(alink)
            if page is None:
                continue
            html = BeautifulSoup(page)
            links = html.findAll('a')
            print '获取到的连接数:',len(links)
            for l in links:
                    link = l.get('href').encode('utf-8')
                    if 'http:' in link and link not in urlList:
                        print '将' + str(link) + '放入队列'
                        self.urlqueue.put(link)
                        urlList.append(link)
            print '目前urllist的长度:',len(urlList)
            sleep(1)

class ParserManager(Thread):
    '消费者,从队列中获取url链接，进行分析'
    def __init__(self,t_name,queue):
        Thread.__init__(self,name = t_name)
        self.urlqueue = queue
    def run(self):
        '开始从队列中获取url进行分析'
        print '消费者看到队列大小为:',self.urlqueue.qsize()
        sleep(10)
        while self.urlqueue.qsize() > 0:
            url = self.urlqueue.get()
            pw = ParserWeb(url)
            print '开始分析url:',url
            res = pw.comParser()
            try:
                print res[0],res[1],res[2],res[3].encode('utf-8'),res[4],res[5].encode('utf-8')
            except UnicodeDecodeError,e:
                print e
                print res
        sleep(1)
if __name__ == '__main__':
    queue = Queue()
    spider = Spider('s1',queue,'http://www.21fj.com')
    parser = ParserManager('p1',queue)
    spider.start()
    parser.start()
    spider.join()
    parser.join()

