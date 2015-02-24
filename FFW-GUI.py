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
        txtUrl = wx.TextCtrl(panel,-1)
        txtUrl.SetMinSize((400,-1))

        topBox.Add(lable,proportion = 0,flag=wx.EXPAND|wx.SHAPED)
        topBox.Add(txtUrl,proportion = 1,flag = wx.EXPAND|wx.RIGHT|wx.LEFT, border = 5)
        ######################################################
        midBox = wx.BoxSizer(wx.HORIZONTAL)
        startBtn = wx.Button(panel, label = '开始')
        self.Bind(wx.EVT_BUTTON,self.OnStart,startBtn)
        endBtn = wx.Button(panel, label = '终止')
        self.Bind(wx.EVT_BUTTON,self.OnEnd,endBtn)
        setBtn = wx.Button(panel, label = '设置')
        self.Bind(wx.EVT_BUTTON,self.OnSetup,setBtn)
        midBox.Add(startBtn,proportion=1,flag=wx.RIGHT)
        midBox.Add(endBtn,proportion=1,flag=wx.RIGHT)
        midBox.Add(setBtn,proportion=1,flag=wx.RIGHT)
        ########################################################
        footBox = wx.BoxSizer(wx.HORIZONTAL)
        footBoxLeft = wx.BoxSizer(wx.VERTICAL)
        flLable = wx.StaticText(panel,-1,'过程:')
        flText = wx.TextCtrl(panel,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
        footBoxLeft.Add(flLable)
        footBoxLeft.Add(flText,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM,border=5)
        footBoxRight = wx.BoxSizer(wx.VERTICAL)
        frLable = wx.StaticText(panel,-1,'详细信息:')
        frText = wx.TextCtrl(panel,style=wx.HSCROLL|wx.VSCROLL|wx.TE_MULTILINE|wx.TE_READONLY)
        footBoxRight.Add(frLable)
        footBoxRight.Add(frText,proportion=1,flag=wx.EXPAND|wx.RIGHT|wx.BOTTOM,border=5)
        ###########################
        footBox.Add(footBoxLeft,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM,border=5)
        footBox.Add(footBoxRight,proportion=1,flag=wx.EXPAND|wx.RIGHT|wx.BOTTOM,border=5)
        ########################################################
        bigBox = wx.BoxSizer(wx.VERTICAL)
        bigBox.Add(titleBox)
        bigBox.Add(topBox,proportion=0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        bigBox.Add(midBox,flag=wx.ALIGN_RIGHT|wx.RIGHT)
        bigBox.Add(footBox,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)
        panel.SetSizer(bigBox)
        #########################################################
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetFieldsCount(3)
        self.statusBar.SetStatusWidths([-2,-2,-1])
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.OnTime,self.timer)
        self.timer.Start(500)

        self.Show()
    def _test(self,event):
        wx.MessageBox('haha','测试提示：')
    def OnTime(self,event):
        t = time.localtime(time.time())
        st = time.strftime('%H:%M:%S',t)
        self.statusBar.SetStatusText(st,2)
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
        wx.MessageBox('构造黑名单特征值','提示:')
    def OnMakeWhiteFet(self,event):
        wx.MessageBox('构造白名单特征值','提示:')
    def OnMakeTrainer(self,event):
        wx.MessageBox('构造样本特征训练库','提示:')
    def OnStart(self,event):
        wx.MessageBox('开始','提示:')
    def OnEnd(self,event):
        wx.MessageBox('终止','提示:')
    def OnSetup(self,event):
        wx.MessageBox('设置','提示:')

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
        self.thd = Worker(self.url)
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



class Worker(threading.Thread):
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
if __name__ == '__main__':
    app = wx.App()
    win = FindFakeWebFrame()
    #win = LookListFrame('查看','List/BlackList.txt')
    #win = UpdateWhiteDialog(None,'更新白名单','http://www.sina.com.cn/ddt/wangzhi/index.html')
    #win = UpdateBlackDialog(None,'更新黑名单','verified_online.xml')
    app.MainLoop()