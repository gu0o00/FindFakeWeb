__author__ = 'guojian'
# coding:utf-8
import wx

class FindFakeWebFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='FindFakeWeb',size=(800,400))
        self.CreateStatusBar()
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

        makeBlackFet = menu2.Append(-1,'构造黑名单特征值')
        self.Bind(wx.EVT_MENU,self._test,makeBlackFet)
        makeWhiteFet = menu2.Append(-1,'构造白名单特征值')
        self.Bind(wx.EVT_MENU,self._test,makeWhiteFet)
        makeTrainer = menu2.Append(-1,'构造样本训练模型')
        self.Bind(wx.EVT_MENU,self._test,makeTrainer)

        menuBar.Append(menu2,'样本训练库')
        self.SetMenuBar(menuBar)
        ######################################################
        

        self.Show()
    def _test(self,event):
        wx.MessageBox('haha','测试提示：')

if __name__ == '__main__':
    app = wx.App()
    win = FindFakeWebFrame()
    app.MainLoop()