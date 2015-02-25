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
import wx
from wx.lib.pubsub import Publisher
from MakeTrain import MakeSVMFormat
from predict import predict
class Spider(Thread):
    '生产者，爬取url链接放入队列'
    def __init__(self, t_name, queue, starturl):
        Thread.__init__(self, name = t_name)
        self.urlqueue = queue
        self.starturl = starturl
        self.is_alive = True
    def run(self):
        #print '正在下载初始页面'
        wx.CallAfter(Publisher().sendMessage,'UpdateProc','正在下载初始页面')
        page = DownloadWeb(self.starturl)
        if page is None:
            #print '初始页面下载失败'
            wx.CallAfter(Publisher().sendMessage,'UpdateProc','初始页面下载失败')
            return
        links = GetLinks(page)
        for alink in links:
            self.urlqueue.put(alink)
        urlList = []
        urlList += links
        i = 0
        while len(urlList) > i and self.is_alive:
            alink = urlList[i]
            i += 1
            #print '\033[1;31;40m'
            #print '正在下载:',alink
            wx.CallAfter(Publisher().sendMessage,'UpdateProc','正在下载:'+str(alink))
            page = DownloadWeb(alink)
            if page is None:
                #print '获取页面失败',alink
                wx.CallAfter(Publisher().sendMessage,'UpdateProc','获取页面失败'+str(alink))
                continue
            links = GetLinks(page)
            #print '获取到的连接数:',len(links)
            wx.CallAfter(Publisher().sendMessage,'UpdateProc','获取到的连接数:'+str(len(links)))
            count = 0
            for link in links:
                if 'http:' in link and link not in urlList and self.is_alive:
                    self.urlqueue.put(link)
                    urlList.append(link)
                    count += 1
            print '目前urllist的长度:',len(urlList)
            wx.CallAfter(Publisher().sendMessage,'UpdateUrlNum',count)
            sleep(1)

class ParserManager(Thread):
    '消费者,从队列中获取url链接，进行分析'
    def __init__(self,t_name,queue):
        Thread.__init__(self,name = t_name)
        self.urlqueue = queue
        self.is_alive = True
    def run(self):
        '开始从队列中获取url进行分析'
        print '消费者看到队列大小为:',self.urlqueue.qsize()
        url = ''
        sleep(30)  #根据网速决定延时，应该大于下载首个网页的时间
        while self.urlqueue.qsize() > 0 and self.is_alive:
            try:
                file_res = open('result.log','a')
                print '\033[0m'
                print '消费者看到队列大小为:',self.urlqueue.qsize()
                url = self.urlqueue.get()
                pw = ParserWeb(url)
                #print '开始分析url:',url
                wx.CallAfter(Publisher().sendMessage,'UpdateUrlNum',-1)
                wx.CallAfter(Publisher().sendMessage,'UpdateInfo','开始分析url:'+str(url))
                res = pw.comParser()
                #print res[0],res[1],res[2],res[3].encode('utf-8'),res[4],res[5]
                tofile = str(res[0]) + os.linesep                   #url
                tofile += str(res[1]) + ','                         #是否包含ip地址
                tofile += str(res[2]) + ','                         #url中下划线的数量
                tofile +=  unicode(res[3]).encode('utf-8') + ','    #ICP号
                tofile +=  str(res[4]) + ','                        #链接统计
                tofile += unicode(res[5]).encode('utf-8')           #注册年龄
                #表单数
                #图片数
                #url长度
                file_res.write(tofile + os.linesep)
                file_res.close()
                ###############实现机器识别#################################
                parse_res = MakeSVMFormat(res)
                res = predict(parse_res)
                if res < 0:
                    wx.CallAfter(Publisher().sendMessage,'UpdateFakeNum',1)
                wx.CallAfter(Publisher().sendMessage,'UpdateInfo','结果:'+tofile)
            except UnicodeEncodeError,e:
                file_res.close()
                print 'UnicodeEncodeError:',
                print e.reason
                print res
                wx.CallAfter(Publisher().sendMessage,'UpdateInfo','网页分析失败:'+str(url))
            except Exception,e:
                file_res.close()
                print '出现异常:',e
                wx.CallAfter(Publisher().sendMessage,'UpdateInfo','网页分析失败:'+str(url))
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

