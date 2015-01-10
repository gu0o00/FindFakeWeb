# coding:utf-8

from xml.sax.handler import ContentHandler
from xml.sax import parse

class HandleXML(ContentHandler):
    def __init__(self):
        self.inlist = []
        self.__isurl__ = False

    def startElement(self, name, attrs):
        #print 'name:',name, 'attrs:',attrs.keys()
        if name == 'url':
            self.__isurl__ = True

    def endElement(self, name):
        #print 'endname:',name
        #print
        pass

    def characters(self, content):
        content = content.strip()
        if len(content)>0 and self.__isurl__:
            #print 'chars',content
            self.inlist.append(content)
            self.__isurl__ = False

def parserXML(xml):
    xmlparser = HandleXML()
    parse(xml,xmlparser)
    return xmlparser.inlist

if __name__ == '__main__':
    resList = parserXML('verified_online.xml.bak')
    BlackFile = open('List/BlackList.txt','w')
    import os
    for item in resList:
        BlackFile.write(item + os.linesep)
    BlackFile.close()
