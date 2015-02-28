__author__ = 'guojian'
# coding:utf-8
from ParserWeb import ParserWeb
import os
def TrainWhite(filename = 'List/WhiteList.txt'):
    WhtFile = open(filename,'r')
    allLinks = WhtFile.readlines()
    count = 0

    WhtTrain = open('train/White.train','w')
    for aLink in allLinks:
        #print aLink
        pw = ParserWeb(aLink)
        res = pw.comParser()
        ########################
        alineres = '1 '
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
        if res[4][0] < 10 :     #如果网页链接数小于10,则舍弃这个页面
            continue
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
        alineres += "8:" + str(res[6]) + " "
        alineres += "9:" + str(res[7]) + " "
        alineres += "10:" + str(res[8]) + " "
        ########################
        print res
        WhtTrain.write(alineres + os.linesep)
        count += 1
        print '白名单构造向量特征训练库完成第' + str(count) + '个'
    WhtTrain.close()

def TrainBlack(filename = 'List/BlackList.txt'):
    BlkFile = open(filename,'r')
    allLinks = BlkFile.readlines()
    count = 0

    BlkTrain = open('train/Black.train','w')
    for aLink in allLinks:
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
        alineres += "7:" + str(res[5]) + " "
        alineres += "8:" + str(res[6]) + " "
        alineres += "9:" + str(res[7]) + " "
        alineres += "10:" + str(res[8]) + " "
        ########################
        print res
        BlkTrain.write(alineres + os.linesep)
        count += 1
        print '黑名单构造向量特征训练库完成第' + str(count) + '个'
    BlkTrain.close()
def MakeSVMFormat(parse_res):
    res = parse_res
    dictList = []
    aDict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
    ########################
    alineres = '-1 '
    if res[1] == False:
        aDict[1] = 0
    else :
        aDict[1] = 1
    ########################
    aDict[2] = res[2]
    ########################
    #print res[3]
    if res[3] == "该网站暂无备案" or res[3] == None:
        aDict[3] = 0
    else :
        aDict[3] = 1
    ########################
    aDict[4] = res[4][0]
    aDict[5] = res[4][1]
    aDict[6] = res[4][2]
    ########################
    try:
        time_str = res[5]
        year = time_str.split('年'.decode('utf-8'))
        month = year[1].split('月'.decode('utf-8'))
        day = month[1].split('天'.decode('utf-8'))
        time = int(year[0]) * 365 + int(month[0]) * 30 + int(day[0])
    except :
        time = '0 '
    aDict[7] = time
    ########################
    aDict[8] = res[6]
    aDict[9] = res[7]
    aDict[10] = res[8]
    ########################
    dictList.append(aDict)
    return dictList


if __name__ == '__main__':
    #import threading
    #class MyThread(threading.Thread):
    #    def __init__(self,t_name,func):
    #        threading.Thread.__init__(self)
    #        self.func = func
    #    def run(self):
    #        self.func()
    #t1 = MyThread('White',TrainWhite)
    #t2 = MyThread('Black',TrainBlack)
    #t1.start()
    #t2.start()
    #t1.join()
    #t2.join()

    TrainWhite()
    #TrainBlack()

