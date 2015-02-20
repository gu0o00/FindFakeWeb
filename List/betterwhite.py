import os

wf = open('WhiteList.txt','r')
fl = open('List.txt','a')

allines = wf.readlines()
for a in allines:
    if 'sina' not in a:
        fl.write(a)

wf.close()
fl.close()
