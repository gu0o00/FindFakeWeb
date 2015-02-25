__author__ = 'guojian'
# coding:utf-8
import wx
import time,os,threading
from wx.lib.pubsub import Publisher

class FindFakeWebFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='FindFakeWeb',size=(800,400))
        panel = wx.Panel(self)
        ####################生成菜单项########################################
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()

        lookBlackList = menu1.Append(-1,'查看黑名单')
        self.Bind(wx.EVT_MENU,self.OnLookBlackList,lookBlackList)
        updateBlackList = menu1.Append(-1,'更新黑名单')
        self.Bind(wx.EVT_MENU,self.OnUpdateBlackList,updateBlackList)

        menu1.AppendSeparator()

        lookWhitelist = menu1.Append(-1,'查看白名单')
        self.Bind(wx.EVT_MENU,self.OnLookWhiteList,lookWhitelist)
        updateWhitelist = menu1.Append(-1,'更新白名单')
        self.Bind(wx.EVT_MENU,self.OnUpdateWhiteList,updateWhitelist)

        menuBar.Append(menu1,'黑白名单')
        menu2 = wx.Menu()

        makeBlackFet = menu2.Append(-1,'构造黑名单特征值','aa')
        self.Bind(wx.EVT_MENU,self.OnMakeBlackFet,makeBlackFet)
        makeWhiteFet = menu2.Append(-1,'构造白名单特征值')
        self.Bind(wx.EVT_MENU,self.OnMakeWhiteFet,makeWhiteFet)
        makeTrainer = menu2.Append(-1,'构造样本训练模型')
        self.Bind(wx.EVT_MENU,self.OnMakeTrainer,makeTrainer)

        menuBar.Append(menu2,'样本训练库')
        self.SetMenuBar(menuBar)
        ######################################################
        titleBox = wx.BoxSizer(wx.VERTICAL)
        topTitle = wx.StaticText(panel,-1,'Find Fake Web')
        topTitle.SetFont(wx.Font(18,wx.SW_3D,wx.NORMAL,wx.BOLD))
        topLine = wx.StaticLine(panel,-1,wx.DefaultPosition,wx.DefaultSize)
        titleBox.Add(topTitle,0,wx.ALL,5)
        titleBox.Add(topLine,0,wx.EXPAND|wx.TOP|wx.SHAPED,5)
        ######################################################
        topBox = wx.BoxSizer(wx.HORIZONTAL)

        lable = wx.StaticText(panel, -1, '爬虫开始的URL:')
        self.txtUrl = wx.TextCtrl(panel,-1)
        self.txtUrl.SetMinSize((400,-1))

        topBox.Add(lable,proportion = 0,flag=wx.EXPAND|wx.SHAPED)
        topBox.Add(self.txtUrl,proportion = 1,flag = wx.EXPAND|wx.RIGHT|wx.LEFT, border = 5)
        ######################################################
        midBox = wx.BoxSizer(wx.HORIZONTAL)
        self.startBtn = wx.Button(panel, label = '开始')
        self.Bind(wx.EVT_BUTTON,self.OnStart,self.startBtn)
        endBtn = wx.Button(panel, label = '终止')
        self.Bind(wx.EVT_BUTTON,self.OnEnd,endBtn)
        setBtn = wx.Button(panel, label = '设置')
        self.Bind(wx.EVT_BUTTON,self.OnSetup,setBtn)
        midBox.Add(self.startBtn,proportion=1,flag=wx.RIGHT)
        midBox.Add(endBtn,proportion=1,flag=wx.RIGHT)
        midBox.Add(setBtn,proportion=1,flag=wx.RIGHT)
        ########################################################
        footBox = wx.BoxSizer(wx.HORIZONTAL)
        footBoxLeft = wx.BoxSizer(wx.VERTICAL)
        flLable = wx.StaticText(panel,-1,'过程:')
        self.flText = wx.TextCtrl(panel,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
        footBoxLeft.Add(flLable)
        footBoxLeft.Add(self.flText,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM,border=5)
        footBoxRight = wx.BoxSizer(wx.VERTICAL)
        frLable = wx.StaticText(panel,-1,'详细信息:')
        self.frText = wx.TextCtrl(panel,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
        footBoxRight.Add(frLable)
        footBoxRight.Add(self.frText,proportion=1,flag=wx.EXPAND|wx.RIGHT|wx.BOTTOM,border=5)
        ###########################
        footBox.Add(footBoxLeft,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM,border=5)
        footBox.Add(footBoxRight,proportion=1,flag=wx.EXPAND|wx.RIGHT|wx.BOTTOM,border=5)
        ###########################
        self.fakeUrlTxt = wx.TextCtrl(panel,-1,value='如果发现可疑链接将在此显示',style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
        self.fakeUrlTxt.SetMaxSize((-1,80))
        ########################################################
        bigBox = wx.BoxSizer(wx.VERTICAL)
        bigBox.Add(titleBox)
        bigBox.Add(topBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(midBox,flag=wx.ALIGN_RIGHT|wx.RIGHT)
        bigBox.Add(footBox,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        bigBox.Add(self.fakeUrlTxt,proportion=1,flag=wx.EXPAND|wx.BOTTOM,border=10)
        panel.SetSizer(bigBox)
        #########################################################
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(4)
        self.statusBar.SetStatusWidths([-2,-2,-2,-1])
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.OnTime,self.timer)
        self.timer.Start(500)

        Publisher().subscribe(self.UpdateProc,'UpdateProc') #接收生产者spider的消息
        Publisher().subscribe(self.UpdateInfo,'UpdateInfo') #接收消费者parser的消息
        Publisher().subscribe(self.UpdateStatus1,'UpdateUrlNum') #显示队列中剩余的链接数
        Publisher().subscribe(self.UpdateStatus2,'UpdateFakeNum') #显示发现的可疑链接数

        self.Show()
    def _test(self,event):
        wx.MessageBox('haha','测试提示：')
    def OnTime(self,event):
        t = time.localtime(time.time())
        st = time.strftime('%H:%M:%S',t)
        self.statusBar.SetStatusText(st,3)
    def OnLookBlackList(self,event):
        #wx.MessageBox('查看黑名单','提示:')
        win = LookListFrame(self,'查看','List/BlackList.txt')
        win.ShowModal()
    def OnUpdateBlackList(self,event):
        #wx.MessageBox('更新黑名单','提示:')
        win = UpdateBlackDialog(None,'更新黑名单','verified_online.xml')
        win.ShowModal()
    def OnLookWhiteList(self,event):
        #wx.MessageBox('查看白名单','提示:')
        win = LookListFrame(self,'查看','List/WhiteList.txt')
        win.ShowModal()
    def OnUpdateWhiteList(self,event):
        #wx.MessageBox('更新白名单','提示:')
        win = UpdateWhiteDialog(self,'更新白名单','http://www.sina.com.cn/ddt/wangzhi/index.html')
        win.ShowModal()
    def OnMakeBlackFet(self,event):
        #wx.MessageBox('构造黑名单特征值','提示:')
        win = MakeBlackFetDialog(self,'更新黑名单样本训练库','List/BlackList.txt')
        win.ShowModal()
    def OnMakeWhiteFet(self,event):
        #wx.MessageBox('构造白名单特征值','提示:')
        win = MakeWhiteFetDialog(self,'更新白名单样本训练库','List/WhiteList.txt')
        win.ShowModal()
    def OnMakeTrainer(self,event):
        #wx.MessageBox('构造样本特征训练库','提示:')
        win = MakeModel(self)
        win.ShowModal()
    def OnStart(self,event):
        #wx.MessageBox('开始','提示:')
        self.txtUrl.SetValue('http://www.sohu.com')
        startUrl = str(self.txtUrl.Value)
        self.finishCount = 1
        self.urlCount = 0
        self.fakeCount = 0
        import SpiderGUI
        from Queue import Queue
        self.queue = Queue()
        self.spider = SpiderGUI.Spider('s1',self.queue,startUrl)
        self.parser = SpiderGUI.ParserManager('p1',self.queue)
        self.spider.start()
        self.parser.start()
        #self.spider.join()
        #self.parser.join()
        self.startBtn.Disable()
    def OnEnd(self,event):
        #wx.MessageBox('终止','提示:')
        self.spider.is_alive = False
        self.parser.is_alive = False
        self.startBtn.Enable()
    def OnSetup(self,event):
        wx.MessageBox('设置','提示:')
    def UpdateProc(self,msg):
        info = str(msg.data)
        self.flText.SetValue(self.flText.Value.encode('utf-8')+info+os.linesep)
        self.flText.ShowPosition(self.flText.GetLastPosition())
    def UpdateInfo(self,msg):
        info = str(msg.data)
        self.frText.SetValue(self.frText.Value.encode('utf-8')+info+os.linesep)
        self.frText.ShowPosition(self.frText.GetLastPosition())
        self.statusBar.SetStatusText('已经分析完成:' + str(self.finishCount),1)
        self.finishCount += 1
    def UpdateStatus1(self,msg):
        num = int(msg.data)
        self.urlCount += num
        self.statusBar.SetStatusText('队列中URL数量'+str(self.urlCount),0)
    def UpdateStatus2(self,msg):
        num = int(msg.data)
        self.fakeCount += num
        self.statusBar.SetStatusText('已发现可疑网站数量:'+str(self.fakeCount)+'个')


class LookListFrame(wx.Dialog):
    def __init__(self,parent,title,filepath):
        wx.Dialog.__init__(self,parent,title = title,size=(600,200))
        self.path = filepath
        self.panel = wx.Panel(self)
        self.cont = wx.TextCtrl(self.panel,-1,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE)

        filecont = open(os.getcwd()+os.sep+filepath).read()

        self.cont.SetValue(filecont)
        self.saveBtn = wx.Button(self.panel,-1,label='保存')
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.saveBtn)
        self.clearBtn = wx.Button(self.panel,-1,label='清空')
        self.Bind(wx.EVT_BUTTON,self.OnClear,self.clearBtn)
        self.closeBtn = wx.Button(self.panel,-1,label='关闭')
        self.Bind(wx.EVT_BUTTON,self.OnClose,self.closeBtn)
        self.footBox = wx.BoxSizer(wx.HORIZONTAL)
        self.footBox.Add(self.saveBtn,proportion=0,flag=wx.CENTER|wx.BOTTOM)
        self.footBox.Add(self.clearBtn,proportion=0,flag=wx.CENTER|wx.BOTTOM)
        self.footBox.Add(self.closeBtn,proportion=0,flag=wx.CENTER|wx.BOTTOM)
        self.wholeBox = wx.BoxSizer(wx.VERTICAL)
        self.wholeBox.Add(self.cont,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT)
        self.wholeBox.Add(self.footBox,proportion=0,flag=wx.CENTER|wx.BOTTOM)
        self.panel.SetSizer(self.wholeBox)
        self.Show()
    def OnSave(self,event):
        cont = self.cont.GetValue()
        print os.getcwd()+os.sep+self.path
        fp = open(os.getcwd()+os.sep+self.path,'w')
        fp.write(cont)
        fp.close()
    def OnClear(self,event):
        fp = open(os.getcwd()+os.sep+self.path,'w')
        fp.write('')
        self.cont.SetValue('')
        fp.close()
    def OnClose(self,event):
        self.Close()

class UpdateWhiteDialog(wx.Dialog):
    def __init__(self,parent,title,url):
        wx.Dialog.__init__(self,parent,title = title,size=(400,200))
        self.url = url
        self.panel = wx.Panel(self)

        topBox = wx.BoxSizer(wx.HORIZONTAL)
        txtLbl = wx.StaticText(self.panel,-1,'爬虫开始url:')
        self.urlTxt = wx.TextCtrl(self.panel,-1,value=self.url)
        topBox.Add(txtLbl,proportion=0,flag=wx.LEFT,border=5)
        topBox.Add(self.urlTxt,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=5)

        self.cont = wx.TextCtrl(self.panel,-1,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)

        midBox = wx.BoxSizer(wx.HORIZONTAL)
        midBox.Add(self.cont,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)

        footBox = wx.BoxSizer(wx.HORIZONTAL)
        self.updateBtn = wx.Button(self.panel,-1,label='更新')
        self.Bind(wx.EVT_BUTTON,self.OnUpdate,self.updateBtn)
        self.endBtn = wx.Button(self.panel,-1,label='停止')
        self.Bind(wx.EVT_BUTTON,self.OnEnd,self.endBtn)
        self.info = wx.StaticText(self.panel,-1)

        footBox.Add(self.updateBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.endBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.info,proportion=0,flag=wx.EXPAND|wx.LEFT,border=5)

        bigBox = wx.BoxSizer(wx.VERTICAL)
        bigBox.Add(topBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(midBox,proportion=1,flag=wx.EXPAND)
        bigBox.Add(footBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        self.panel.SetSizer(bigBox)

        self.Show()
        Publisher().subscribe(self.UpdateDisplay,'update')
    def OnUpdate(self,event):
        self.thd = UpdateWhiteListWorker(self.url)
        self.thd.start()
        self.updateBtn.Disable()
    def OnEnd(self,event):
        self.thd.is_alive = False
        self.updateBtn.Enable()
        links = str(self.cont.Value).split('\n')
        fp = open('List/WhiteList.txt','w')
        for alink in links:
            fp.write(alink+os.linesep)
        fp.close()
        self.info.SetLabel('获取的链接结果已写入文件')
    def UpdateDisplay(self,msg):
        self.cont.Value += str(msg.data) + '\n'
        self.cont.ShowPosition(self.cont.GetLastPosition())
        count = len(str(self.cont.Value).split('\n'))
        self.info.SetLabel('已得到连接数：' + str(count))
        pass

class UpdateBlackDialog(wx.Dialog):
    def __init__(self,parent,title,path='verified_online.xml'):
        wx.Dialog.__init__(self,parent = parent,title= title,size=(400,200))
        self.path = path

        self.panel = wx.Panel(self)

        topBox = wx.BoxSizer(wx.HORIZONTAL)
        txtLbl = wx.StaticText(self.panel,-1,'xml文件所在路径:')
        self.pathTxt = wx.TextCtrl(self.panel,-1,value=self.path)
        topBox.Add(txtLbl,proportion=0,flag=wx.LEFT,border=5)
        topBox.Add(self.pathTxt,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=5)

        self.cont = wx.TextCtrl(self.panel,-1,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)

        midBox = wx.BoxSizer(wx.HORIZONTAL)
        midBox.Add(self.cont,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)

        footBox = wx.BoxSizer(wx.HORIZONTAL)
        self.updateBtn = wx.Button(self.panel,-1,label='更新')
        self.Bind(wx.EVT_BUTTON,self.OnUpdate,self.updateBtn)
        self.saveBtn = wx.Button(self.panel,-1,label='保存')
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.saveBtn)
        self.info = wx.StaticText(self.panel,-1)

        footBox.Add(self.updateBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.saveBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.info,proportion=0,flag=wx.EXPAND|wx.LEFT,border=5)

        bigBox = wx.BoxSizer(wx.VERTICAL)
        bigBox.Add(topBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(midBox,proportion=1,flag=wx.EXPAND)
        bigBox.Add(footBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        self.panel.SetSizer(bigBox)

        self.Show()
    def OnUpdate(self,event):
        from GetBlackList import parserXML
        self.resList = parserXML(self.path)
        self.info.SetLabel('获取到钓鱼网站URL'+str(len(resList))+'个')
        for alink in self.resList:
            self.cont.Value += str(alink) + os.linesep
        self.cont.SetPosition(self.cont.GetLastPosition())
    def OnSave(self,event):
        fp = open('List/BlackList.txt','w')
        for alink in self.resList:
            fp.write(alink + os.linesep)
        fp.close()

class UpdateWhiteListWorker(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.is_alive = True
        self.url = url
    def run(self):
        linklist = []
        middlelist = []
        from BeautifulSoup import BeautifulSoup
        from DownLoadWeb import DownloadWeb
        startUrl = self.url
        page = DownloadWeb(startUrl)
        assert isinstance (page,str )
        html = BeautifulSoup(page)
        for link in html.findAll('a'):
            if not self.is_alive:
                break
            link = unicode(link.get('href')).encode('utf8')
            if link.startswith('http') and 'sina' not in link:
                linklist.append(link)
                wx.CallAfter(Publisher().sendMessage,'update',str(link))
            elif 'sina' not in link:
                middlelist.append(link)
        url = '/'.join(startUrl.split('/')[:-1])
        for elink in middlelist:
            if not self.is_alive:
                break
            aurl = url + '/' + elink
            print aurl
            page = DownloadWeb(aurl)
            assert isinstance (page,str )
            html = BeautifulSoup(page)
            for link in html.findAll('a'):
                if not self.is_alive:
                    break
                link = unicode(link.get('href').encode('utf8'))
                linklist.append(link)
                wx.CallAfter(Publisher().sendMessage,'update',str(link))

class MakeBlackFetDialog(wx.Dialog):
    def __init__(self,parent,title,path):
        wx.Dialog.__init__(self,parent,title = title,size=(600,400))
        self.path = path
        self.panel = wx.Panel(self)

        topBox = wx.BoxSizer(wx.HORIZONTAL)
        txtLbl = wx.StaticText(self.panel,-1,'黑名单所在路径:')
        self.urlTxt = wx.TextCtrl(self.panel,-1,value=self.path)
        topBox.Add(txtLbl,proportion=0,flag=wx.LEFT,border=5)
        topBox.Add(self.urlTxt,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=5)

        self.cont = wx.TextCtrl(self.panel,-1,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)

        midBox = wx.BoxSizer(wx.HORIZONTAL)
        midBox.Add(self.cont,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)

        footBox = wx.BoxSizer(wx.HORIZONTAL)
        self.updateBtn = wx.Button(self.panel,-1,label='更新')
        self.Bind(wx.EVT_BUTTON,self.OnUpdate,self.updateBtn)
        self.endBtn = wx.Button(self.panel,-1,label='停止')
        self.Bind(wx.EVT_BUTTON,self.OnEnd,self.endBtn)
        self.info = wx.StaticText(self.panel,-1)

        footBox.Add(self.updateBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.endBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.info,proportion=0,flag=wx.EXPAND|wx.LEFT,border=5)

        bigBox = wx.BoxSizer(wx.VERTICAL)
        bigBox.Add(topBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(midBox,proportion=1,flag=wx.EXPAND)
        bigBox.Add(footBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        self.panel.SetSizer(bigBox)

        self.Show()
        Publisher().subscribe(self.UpdateDisplay,'UpdateBlackTrainer')
    def OnUpdate(self,event):
        self.thd = UpdateBlackTrainerWorker(self.path)
        self.thd.start()
        self.count = 0
        self.updateBtn.Disable()
    def OnEnd(self,event):
        self.thd.is_alive = False
        self.updateBtn.Enable()
    def UpdateDisplay(self,msg):
        txt = str(msg.data)
        if not txt.startswith('#'):
            self.cont.Value += txt + os.linesep
            self.count += 1
        else:
            self.cont.SetValue(str(self.cont.Value) + txt)
        self.info.SetLabel('已经完成'+str(self.count)+'个')

class UpdateBlackTrainerWorker(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.is_alive = True
        self.path = path
    def run(self):
        from ParserWeb import ParserWeb
        filename = self.path
        BlkFile = open(filename,'r')
        allLinks = BlkFile.readlines()
        #count = 0

        BlkTrain = open('train/Black.train','w')
        for aLink in allLinks:
            if not self.is_alive:
                break
            #print aLink
            pw = ParserWeb(aLink,True)
            res = pw.comParser()
            ########################
            alineres = '-1 '
            if res[1] == False:
                alineres += '1:0 '
            else :
                alineres += '1:1 '
            ########################
            alineres += "2:" + str(res[2]) + " "
            ########################
            #print res[3]
            if res[3] == "该网站暂无备案" or res[3] == None:
                alineres += '3:0 '
            else :
                alineres += '3:1 '
            ########################
            alineres += "4:" + str(res[4][0]) + " "
            alineres += "5:" + str(res[4][1]) + " "
            alineres += "6:" + str(res[4][2]) + " "
            ########################
            try:
                time_str = res[5]
                year = time_str.split('年'.decode('utf-8'))
                month = year[1].split('月'.decode('utf-8'))
                day = month[1].split('天'.decode('utf-8'))
                time = int(year[0]) * 365 + int(month[0]) * 30 + int(day[0])
            except :
                time = '0 '
            alineres += "7:" + str(time) + " "
            ########################
            print res
            BlkTrain.write(alineres + os.linesep)
            #count += 1
            #print '黑名单构造向量特征训练库完成第' + str(count) + '个'
            wx.CallAfter(Publisher().sendMessage,'UpdateBlackTrainer',str(aLink) + str(alineres))
        BlkTrain.close()
        wx.CallAfter(Publisher().sendMessage,'UpdateBlackTrainer',str('#结果已写入文件'))

class MakeWhiteFetDialog(wx.Dialog):
    def __init__(self,parent,title,path):
        wx.Dialog.__init__(self,parent,title = title,size=(600,400))
        self.path = path
        self.panel = wx.Panel(self)

        topBox = wx.BoxSizer(wx.HORIZONTAL)
        txtLbl = wx.StaticText(self.panel,-1,'白名单所在路径:')
        self.urlTxt = wx.TextCtrl(self.panel,-1,value=self.path)
        topBox.Add(txtLbl,proportion=0,flag=wx.LEFT,border=5)
        topBox.Add(self.urlTxt,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=5)

        self.cont = wx.TextCtrl(self.panel,-1,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)

        midBox = wx.BoxSizer(wx.HORIZONTAL)
        midBox.Add(self.cont,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)

        footBox = wx.BoxSizer(wx.HORIZONTAL)
        self.updateBtn = wx.Button(self.panel,-1,label='更新')
        self.Bind(wx.EVT_BUTTON,self.OnUpdate,self.updateBtn)
        self.endBtn = wx.Button(self.panel,-1,label='停止')
        self.Bind(wx.EVT_BUTTON,self.OnEnd,self.endBtn)
        self.info = wx.StaticText(self.panel,-1)

        footBox.Add(self.updateBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.endBtn,proportion=0,flag=wx.ALIGN_RIGHT,border=5)
        footBox.Add(self.info,proportion=0,flag=wx.EXPAND|wx.LEFT,border=5)

        bigBox = wx.BoxSizer(wx.VERTICAL)
        bigBox.Add(topBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(midBox,proportion=1,flag=wx.EXPAND)
        bigBox.Add(footBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        self.panel.SetSizer(bigBox)

        self.Show()
        Publisher().subscribe(self.UpdateDisplay,'UpdateWhiteTrainer')
    def OnUpdate(self,event):
        self.thd = UpdateWhiteTrainerWorker(self.path)
        self.thd.start()
        self.count = 0
        self.updateBtn.Disable()
    def OnEnd(self,event):
        self.thd.is_alive = False
        self.updateBtn.Enable()
    def UpdateDisplay(self,msg):
        txt = str(msg.data)
        if not txt.startswith('#'):
            self.cont.Value += txt + os.linesep
            self.count += 1
        else:
            self.cont.SetValue(str(self.cont.Value) + txt)
        self.info.SetLabel('已经完成'+str(self.count)+'个')

class UpdateWhiteTrainerWorker(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.is_alive = True
        self.path = path
    def run(self):
        from ParserWeb import ParserWeb
        filename = self.path
        BlkFile = open(filename,'r')
        allLinks = BlkFile.readlines()
        #count = 0

        BlkTrain = open('train/White.train','w')
        for aLink in allLinks:
            if not self.is_alive:
                break
            #print aLink
            pw = ParserWeb(aLink)
            res = pw.comParser()
            ########################
            alineres = '1 '             ##如果直接复用代码，别忘了修改这里
            if res[1] == False:
                alineres += '1:0 '
            else :
                alineres += '1:1 '
            ########################
            alineres += "2:" + str(res[2]) + " "
            ########################
            #print res[3]
            if res[3] == "该网站暂无备案" or res[3] == None:
                alineres += '3:0 '
            else :
                alineres += '3:1 '
            ########################
            alineres += "4:" + str(res[4][0]) + " "
            alineres += "5:" + str(res[4][1]) + " "
            alineres += "6:" + str(res[4][2]) + " "
            ########################
            try:
                time_str = res[5]
                year = time_str.split('年'.decode('utf-8'))
                month = year[1].split('月'.decode('utf-8'))
                day = month[1].split('天'.decode('utf-8'))
                time = int(year[0]) * 365 + int(month[0]) * 30 + int(day[0])
            except :
                time = '0 '
            alineres += "7:" + str(time) + " "
            ########################
            print res
            BlkTrain.write(alineres + os.linesep)
            #count += 1
            #print '白名单构造向量特征训练库完成第' + str(count) + '个'
            wx.CallAfter(Publisher().sendMessage,'UpdateWhiteTrainer',str(aLink) + str(alineres))
        BlkTrain.close()
        wx.CallAfter(Publisher().sendMessage,'UpdateWhiteTrainer',str('#结果已写入文件'))

class MakeModel(wx.Dialog):
    def __init__(self,parent,title='构造训练模型'):
        wx.Dialog.__init__(self,parent=parent,title=title,size=(400,300))
        panel = wx.Panel(self)

        bBox = wx.BoxSizer(wx.HORIZONTAL)
        bLabel = wx.StaticText(panel,-1,label='黑名单路径:')
        self.bTxt = wx.TextCtrl(panel,-1,value='train/Black.train')
        bBox.Add(bLabel,proportion=0,flag=wx.LEFT,border=5)
        bBox.Add(self.bTxt,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=5)

        wBox = wx.BoxSizer(wx.HORIZONTAL)
        wLable = wx.StaticText(panel,-1,label='白名单路径:')
        self.wTxt = wx.TextCtrl(panel,-1,value='train/White.train')
        wBox.Add(wLable,proportion=0,flag=wx.LEFT,border=5)
        wBox.Add(self.wTxt,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=5)

        infoLabel = wx.StaticText(panel,-1,label='详细信息:')
        self.infoTxt = wx.TextCtrl(panel,-1,style=wx.HSCROLL|wx.VSCROLL|wx.TE_READONLY|wx.TE_MULTILINE)

        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        updateBtn = wx.Button(panel,-1,'更新')
        self.Bind(wx.EVT_BUTTON,self.OnUpdate,updateBtn)
        endBtn = wx.Button(panel,-1,'退出')
        self.Bind(wx.EVT_BUTTON,self.OnEnd,endBtn)
        btnBox.Add(updateBtn,proportion=0)
        btnBox.Add(endBtn,proportion=0)

        bigBox = wx.BoxSizer(wx.VERTICAL)
        bigBox.Add(bBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(wBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(infoLabel,proportion=0,flag=wx.LEFT,border=5)
        bigBox.Add(self.infoTxt,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        bigBox.Add(btnBox,proportion=0,flag=wx.CENTER)

        panel.SetSizer(bigBox)
        self.Show()
    def OnUpdate(self,event):
        import sys
        import string
        sys.path.append('/home/guojian/Workspaces/FindFakeWeb/libsvm/python')
        import svmutil
        self.infoTxt.SetValue(str(self.infoTxt.Value) +'模块导入成功' + os.linesep)
        wtf = open(self.wTxt.Value,'r')
        btf = open(self.bTxt.Value,'r')
        wf = wtf.read()
        bf = btf.read()
        wtf.close()
        btf.close()
        tf = open('train/t.train','w')
        tf.write(wf+bf)
        tf.close()
        self.infoTxt.SetValue(str(self.infoTxt.Value.encode('utf-8'))+wf+bf+os.linesep)
        self.infoTxt.SetValue(str(self.infoTxt.Value.encode('utf-8')) +'文件合并完成' + os.linesep)
        y, x = svmutil.svm_read_problem('train/t.train')
        model = svmutil.svm_train(y, x, '-c 5')
        svmutil.svm_save_model('model_file.model',model)
        self.infoTxt.SetValue(str(self.infoTxt.Value.encode('utf-8')) +'训练模型构造完成，并且保存为文件model_file.model' + os.linesep)
    def OnEnd(self,event):
        self.Close()



if __name__ == '__main__':
    app = wx.App()
    win = FindFakeWebFrame()
    #win = LookListFrame('查看','List/BlackList.txt')
    #win = UpdateWhiteDialog(None,'更新白名单','http://www.sina.com.cn/ddt/wangzhi/index.html')
    #win = UpdateBlackDialog(None,'更新黑名单','verified_online.xml')
    #win = MakeWhiteFetDialog(None,'更新白名单样本训练库','List/WhiteList.txt')
    #win = MakeModel(None)
    app.MainLoop()