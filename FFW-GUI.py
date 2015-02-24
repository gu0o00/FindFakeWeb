__author__ = 'guojian'
# coding:utf-8
import wx
import time

class FindFakeWebFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='FindFakeWeb',size=(800,400))
        panel = wx.Panel(self)
        ####################生成菜单项########################################
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()

        lookBlackList = menu1.Append(-1,'查看黑名单')
        self.Bind(wx.EVT_MENU,self._test,lookBlackList)
        updateBlackList = menu1.Append(-1,'更新黑名单')
        self.Bind(wx.EVT_MENU,self._test,updateBlackList)

        menu1.AppendSeparator()

        lookWhitelist = menu1.Append(-1,'查看白名单')
        self.Bind(wx.EVT_MENU,self._test,lookWhitelist)
        updateWhitelist = menu1.Append(-1,'更新白名单')
        self.Bind(wx.EVT_MENU,self._test,updateWhitelist)

        menuBar.Append(menu1,'黑白名单')
        menu2 = wx.Menu()

        makeBlackFet = menu2.Append(-1,'构造黑名单特征值','aa')
        self.Bind(wx.EVT_MENU,self._test,makeBlackFet)
        makeWhiteFet = menu2.Append(-1,'构造白名单特征值')
        self.Bind(wx.EVT_MENU,self._test,makeWhiteFet)
        makeTrainer = menu2.Append(-1,'构造样本训练模型')
        self.Bind(wx.EVT_MENU,self._test,makeTrainer)

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
        self.Bind(wx.EVT_BUTTON,self._test,startBtn)
        endBtn = wx.Button(panel, label = '终止')
        self.Bind(wx.EVT_BUTTON,self._test,endBtn)
        setBtn = wx.Button(panel, label = '设置')
        self.Bind(wx.EVT_BUTTON,self._test,setBtn)
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

if __name__ == '__main__':
    app = wx.App()
    win = FindFakeWebFrame()
    app.MainLoop()