__author__ = 'guojian'
# coding:utf-8

import sys
sys.path.append('/home/guojian/Workspaces/FindFakeWeb/libsvm/python')
from svmutil import *


if __name__ == '__main__':
    print 'libsvm模块导入成功'
    y, x = svm_read_problem('train/t.train')
    model = svm_train(y, x, '-c 5')
    svm_save_model('model_file.model',model)
    print '完成，程序退出'