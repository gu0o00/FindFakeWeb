__author__ = 'guojian'
# coding:utf-8
from ParserWeb import ParserWeb
import os
def MakeWhiteModel(filename = 'List/WhiteList.txt'):
    WhtFile = open(filename,'r')
    allLinks = WhtFile.readlines()

    WhtModel = open('models/WhiteModel.model','w')
    for aLink in allLinks:
        print aLink
        pw = ParserWeb(aLink)
        res = pw.comParser()
        print res
        ########################
        alineres = '1 '
        if res[1] == False:
            alineres += '1:0 '
        else :
            alineres += '1:1 '
        ########################
        alineres += "2:" + str(res[2]) + " "
        ########################
        print res[3]
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
        WhtModel.write(alineres + os.linesep)
    WhtModel.close()

def MakeBlackModel(filename = 'List/BlackList.txt'):
    BlkFile = open(filename,'r')
    allLinks = BlkFile.readlines()

    BlkModel = open('models/BlackModel.model','w')
    for aLink in allLinks:
        print aLink
        pw = ParserWeb(aLink,True)
        res = pw.comParser()
        print res
        ########################
        alineres = '-1 '
        if res[1] == False:
            alineres += '1:0 '
        else :
            alineres += '1:1 '
        ########################
        alineres += "2:" + str(res[2]) + " "
        ########################
        print res[3]
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
        BlkModel.write(alineres + os.linesep)
    BlkModel.close()

if __name__ == '__main__':
    #MakeWhiteModel()
    MakeBlackModel()

