#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import jieba
import ConfigParser
from bs4 import BeautifulSoup
import jieba.posseg as pseg

reload(sys)
sys.setdefaultencoding("utf-8")


class Process(object):
    """docstring for Process"""

    def __init__(self, cf):
        super(Process, self).__init__()
        self.cf = cf
        self.dataPath = ""

    def parseConf(self):
        self.cf.read("conf.cfg")
        self.dataPath = self.cf.get("data", "dataPath")

    def getPostBody(self, postPath):
        soup = BeautifulSoup(open(postPath))

    def processPageHtm(self, fileList, path):
        pageHtm = "page.htm"
        if pageHtm in fileList:
            pagePath = path + "/" + pageHtm
            soup = BeautifulSoup(open(pagePath))
            postList = soup.find_all("li", "u-forumli")
            postNum = 0
            postPath = path + '/' + 'post' + str(postNum + 1) + '.htm'
            subPostInfo = self.getPostBody(postPath)
            postInfo = {}
            soup2 = BeautifulSoup(str(postList[0]))
            # print soup2.prettify()
            aTag = soup2.find_all('a')
            title = aTag[0].string
            if not soup2.find(class_='userInfo j-userInfo').attrs.has_key('style'):
                name = aTag[1].get('title')
            else:
                name = "anonymous"
            pTag = soup2.find_all('p')
            watch = int(pTag[0].string[-1])
            reply = int(pTag[1].string[-1])
            vote = int(pTag[2].string[-1])
            time = soup2.find(class_='lb10 f-fc9').string
            time = int(''.join(re.findall(r'[0-9]', time)))
            postInfo['name'] = name
            postInfo['title'] = title
            postInfo['time'] = time
            postInfo['watch'] = watch
            postInfo['reply'] = reply
            postInfo['vote'] = vote
            postInfo.update(subPostInfo)
            print postInfo
            # for post in postList:
            #     postNum += 1
            #     postPath = path + '/' + 'post' + str(postNum) + '.htm'
            #     subPostInfo = self.getPostBody(postPath)
            #     postInfo = {}
            #     soup2 = BeautifulSoup(str(post))
            #     # print soup2.prettify()
            #     aTag = soup2.find_all('a')
            #     title = aTag[0].string
            #     if not soup2.find(class_='userInfo j-userInfo').attrs.has_key('style'):
            #         name = aTag[1].get('title')
            #     else:
            #         name = "anonymous"
            #     pTag = soup2.find_all('p')
            #     watch = int(pTag[0].string[-1])
            #     reply = int(pTag[1].string[-1])
            #     vote = int(pTag[2].string[-1])
            #     time = soup2.find(class_='lb10 f-fc9').string
            #     time = int(''.join(re.findall(r'[0-9]', time)))
            #     postInfo['name'] = name
            #     postInfo['title'] = title
            #     postInfo['time'] = time
            #     postInfo['watch'] = watch
            #     postInfo['reply'] = reply
            #     postInfo['vote'] = vote
            #     postInfo.update(subPostInfo)
            #     print postInfo

    def processHtm(self, x):
        path = self.dataPath + "page" + str(x)
        fileList = os.listdir(path)
        self.processPageHtm(fileList, path)

if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    ps = Process(cf)
    ps.parseConf()
    ps.processHtm(8)
