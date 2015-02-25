__author__ = 'guojian'
# coding:utf-8

import sys
sys.path.append('/home/guojian/Workspaces/FindFakeWeb/libsvm/python')
from svmutil import *

def predict(parse_res):
    m = svm_load_model('model_file.model')
    labs,acc,vals = svm_predict([0],parse_res,m)
    return labs[0]

if __name__ == '__main__':
    print 'libsvm模块导入成功'
    svm_read_problem('train/WhiteModel.train')
