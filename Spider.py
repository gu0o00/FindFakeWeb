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
import os
class Spider(Thread):
    '生产者，爬取url链接放入队列'
    def __init__(self, t_name, queue, starturl):
        Thread.__init__(self, name = t_name)
        self.urlqueue = queue
        self.starturl = starturl
    def run(self):
        print '正在下载初始页面'
        page = DownloadWeb(self.starturl)
        if page is None:
            print '初始页面下载失败'
            return
        links = GetLinks(page)
        for alink in links:
            self.urlqueue.put(alink)
        urlList = []
        urlList += links
        i = 0
        while len(urlList) > i:
            alink = urlList[i]
            i += 1
            print '\033[1;31;40m'
            print '正在下载:',alink
            page = DownloadWeb(alink)
            if page is None:
                print '获取页面失败',alink
                continue
            links = GetLinks(page)
            print '获取到的连接数:',len(links)
            for link in links:
                if 'http:' in link and link not in urlList:
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
            try:
                file_res = open('result.log','a')
                print '\033[0m'
                print '消费者看到队列大小为:',self.urlqueue.qsize()
                url = self.urlqueue.get()
                pw = ParserWeb(url)
                print '开始分析url:',url
                res = pw.comParser()
                print res[0],res[1],res[2],res[3].encode('utf-8'),res[4],res[5]
                tofile = str(res[0]) + os.linesep                   #url
                tofile += str(res[1]) + ','                         #是否包含ip地址
                tofile += str(res[2]) + ','                         #url中下划线的数量
                tofile +=  unicode(res[3]).encode('utf-8') + ','    #ICP号
                tofile +=  str(res[4]) + ','                        #链接统计
                tofile += unicode(res[5]).encode('utf-8')           #注册年龄
                file_res.write(tofile + os.linesep)
                file_res.close()
            except UnicodeEncodeError,e:
                file_res.close()
                print 'UnicodeEncodeError:',
                print e.reason
                print res
            except Exception,e:
                file_res.close()
                print '出现异常:',e
        sleep(1)
        print '程序正常退出'
if __name__ == '__main__':
    try:
        queue = Queue()
        spider = Spider('s1',queue,'http://www.sohu.com/')
        parser = ParserManager('p1',queue)
        spider.start()
        parser.start()
        spider.join()
        parser.join()
        spider2 = Spider('s2',queue,'http://blog.sina.com.cn/')
        parser2 = ParserManager('p2',queue)
        spider2.start()
        parser2.start()
        spider2.join()
        parser2.join()
    except KeyboardInterrupt,e:
        print e

