__author__ = 'guojian'
# coding:utf-8

import sys
sys.path.append('/home/guojian/Workspaces/FindFakeWeb/libsvm/python')
from svmutil import *


if __name__ == '__main__':
    print 'libsvm模块导入成功'
    svm_read_problem('train/WhiteModel.train')
