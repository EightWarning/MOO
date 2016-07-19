#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import jieba
import pymongo
import subprocess
import threading
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
        self.coursePath = ""
        self.rawDataPath = ""
        self.jsonDataPath = ""
        self.dbPath = ""
        self.logPath = ""
        self.host = ""
        self.port = 0

    def parseConf(self):
        self.cf.read("config.conf")
        self.coursePath = self.cf.get("courseInfo", "coursePath")
        self.rawDataPath = self.cf.get("courseInfo", "rawDataPath")
        self.jsonDataPath = self.cf.get("courseInfo", "jsonDataPath")
        self.dbPath = self.cf.get("courseInfo", "dbPath")
        self.logPath = self.cf.get("courseInfo", "logPath")
        self.host = self.cf.get("db", "host")
        self.port = self.cf.getint("db", "port")

    def initDb(self):
        if not os.path.exists(self.dbPath):
            os.makedirs(self.dbPath)
        child = subprocess.Popen(["lsof", "-i:27017"], stdout=subprocess.PIPE)
        child.wait()
        out = child.communicate()
        if out[0] == "":
        	dataPath = "--datapath=" + self.dbPath
        	logPath = "--logpath=" + self.logPath
            startMongodb=subprocess.Popen(["mongod",dataPath,logPath],stdout=subprocess.PIPE)
            startMongodb.wait()
            out = startMongodb.communicate()


    def getComments(self, dt):
        comments = []
        i = 0
        for li in dt:
            i += 1
            key = "comment" + str(i)
            tmp = {}
            tmp["body"] = li["body"]
            tmp["votes"] = li["votes"]
            tmp["username"] = li["username"]
            if li["children"]:
                tmp["comments"] = self.getComments(li["children"])
            else:
                tmp["comments"] = []
            item = {}
            item[key] = tmp
            comments.append(item)
        return comments

    def parseJson(self, name):
        postInfo = {}
        with open(name) as f:
            s = json.load(f)
        keys = s["content"].keys()
        content = s["content"]
        postInfo["title"] = content["title"]
        postInfo["threadType"] = content["thread_type"]
        postInfo["time"] = content["created_at"]
        postInfo["username"] = content["username"]
        postInfo["commentNum"] = content["comments_count"]
        postInfo["votes"] = content["votes"]
        postInfo["body"] = content["body"]
        if postInfo["commentNum"] != 0:
            if postInfo["threadType"] == "question":
                postInfo["comments"] = self.getComments(
                    content["non_endorsed_responses"])
            else:
                postInfo["comments"] = self.getComments(content["children"])
        else:
            postInfo["comments"] = []
        j = json.dumps(postInfo)
        jsonName = os.path.join(self.jsonDataPath, os.path.split(name)[1])
        self.saveJson(j, jsonName)

    def saveJson(self, j, name):
        with open(name, 'w') as f:
            f.write(j)

    def delDir(self, path):
        # print path
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            for item in os.listdir(path):
                itemPath = os.path.join(path, item)
                self.delDir(itemPath)
            os.rmdir(path)

    def parseJsons(self):
        self.delDir(self.jsonDataPath)
        print "delDir..."
        os.makedirs(self.jsonDataPath)
        li = os.listdir(self.rawDataPath)
        for p in li:
            threadName = "thread-" + p
            name = os.path.join(self.rawDataPath, p)
            t = threading.Thread(target=self.parseJson,
                                 args=(name,), name=threadName)
            t.start()
            t.join()

if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    ps = Process(cf)
    ps.parseConf()
    ps.parseJsons()
