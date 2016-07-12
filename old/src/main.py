#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import sys
from lib import spider
from lib import textprogress
from sklearn import svm
from sklearn import cross_validation
from sklearn.externals import joblib
import pickle

reload(sys)
sys.setdefaultencoding("utf-8")


def loadxy():
    t = textprogress.TextProgress('test')
    t.segment()
    corpus, y = t.makeMatrix()
    if y and corpus:
        x = t.featureExtraction(corpus)
        # print y
        return x, y


def function():
    pass

if __name__ == '__main__':
    session = requests.Session()
    sp = spider.Spider(session)
    if sp.getPosts():
        print 'getPosts ok'
    else:
        print 'not ok'

    t = textprogress.TextProgress('test')
    if t.segment():
        print 'segment ok'
    x, y = t.makeMatrix()
    if x and y:
        t.featureExtraction(x)
        print 'featureExtraction ok'

    train_data, train_target = loadxy()
    svc = svm.SVC()
    svc_scores = cross_validation.cross_val_score(
        svc, train_data, train_target, cv=5)
    print("svm classifier accuracy:")
    print(svc_scores)

    # joblib.dump(svc, 'svc.model')
    # bin_file = open('svc_bin.data', 'wb')
    # pickle.dump(, bin_file)
    # bin_file.close()
