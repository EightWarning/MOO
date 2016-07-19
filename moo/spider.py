#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import ConfigParser
import requests
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

reload(sys)
sys.setdefaultencoding("utf-8")


class Spider(object):
    """docstring for Spider"""

    def __init__(self, cf, session, driver):
        super(Spider, self).__init__()
        self.cf = cf
        self.homeUrl = ""
        self.loginUrl = ""
        self.prefixUrl = ""
        self.suffixUrl = ""
        self.courseName = ""
        self.courseNameZh = ""
        self.courseId = ""
        self.coursePath = ""
        self.rawDataPath = ""
        self.data = {}
        self.headers = {}
        self.proxies = ""
        self.session = session
        self.driver = driver
        self.localInfo = threading.local()

    def parseConfig(self):
        self.cf.read("config.conf")
        self.homeUrl = self.cf.get("urls", "homeUrl")
        self.loginUrl = self.cf.get("urls", "loginUrl")
        self.prefixUrl = self.cf.get("urls", "prefixUrl")
        self.suffixUrl = self.cf.get("urls", "suffixUrl")
        self.courseName = self.cf.get("courseInfo", "courseName")
        self.courseNameZh = self.cf.get("courseInfo", "courseNameZh")
        self.courseId = self.cf.get("courseInfo", "courseId")
        self.coursePath = self.cf.get("courseInfo", "coursePath")
        self.rawDataPath = self.cf.get("courseInfo", "rawDataPath")
        self.proxies = self.cf.get("proxies", "proxies")
        for item in self.cf.items("userInfo"):
            self.data[item[0]] = item[1]
        for item in self.cf.items("headers"):
            self.headers[item[0]] = item[1]

    def tearDown(self):
        self.driver.quit()

    def getPagenum(self, pageSource):
        pattern = re.compile('''data-thread-pages=".+?"''')
        p = re.compile('''".+?"''').findall(pattern.findall(pageSource)[0])
        page = p[0][1:-1]
        return int(page)

    def getpageBydriver(self):
        self.driver.maximize_window()
        self.driver.get(self.homeUrl)
        time.sleep(2)
        self.driver.find_element_by_id("header_login").click()
        try:
            username = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
        except Exception, e:
            print e
            raise e
        username.send_keys(self.data["username"])
        try:
            password = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
        except Exception, e:
            print e
            raise e
        password.send_keys(self.data["password"])
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id("loginSubmit").click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "html/body/header/div[3]/div/div[2]/div/div[3]/a/img").click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "html/body/div[1]/div[2]/nav/div[1]/ul/li[2]/a").click()
        time.sleep(2)
        self.driver.find_element_by_link_text(self.courseNameZh).click()
        oldHandle = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if oldHandle != handle:
                self.driver.switch_to_window(handle)
                break
        self.driver.find_element_by_xpath(
            "html/body/div[3]/div[2]/nav/div/ol/li[3]/a").click()
        time.sleep(3)
        pages = self.getPagenum(self.driver.page_source)
        for x in xrange(1, pages):
            element = self.driver.find_element_by_class_name(
                "forum-nav-load-more-link")
            element.click()
            print "clicik"
            time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        with open("ppp", 'w') as f:
            f.write(soup.prettify())
        self.tearDown()
        return soup.prettify()

    def getIds(self):
        pageSource = self.getpageBydriver()
        onlyForumList = SoupStrainer(class_="forum-nav-thread-list")
        soup = BeautifulSoup(pageSource, "html.parser",
                             parse_only=onlyForumList)
        items = soup.find_all("li", class_="forum-nav-thread")
        ids = []
        for item in items:
            ids.append(item["data-id"])
        return ids

    def login(self):
        try:
            response = self.session.post(self.loginUrl, data=self.data,
                                         headers=self.headers)
            return response.cookies
        except Exception, e:
            print "login() post error: ", e
            return None

    def delDir(self, path):
        # print path
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            for item in os.listdir(path):
                itemPath = os.path.join(path, item)
                self.delDir(itemPath)
            os.rmdir(path)

    def savePost(self, i, content):
        path = os.path.join(self.rawDataPath, "post" + str(i))
        print path
        with open(path, 'w') as f:
            f.write(content)

    def get(self):
        response = self.session.get(
            self.localInfo.url, cookies=self.localInfo.cookies, headers=self.headers)
        content = response.content
        self.savePost(self.localInfo.i, content)
        print "save...%s" % (threading.current_thread().name)

    def getProcess(self, url, i, cookies):
        self.localInfo.url = url
        self.localInfo.i = i
        self.localInfo.cookies = cookies
        self.get()

    def getPosts(self):
        print "getting posts..."
        self.delDir(self.rawDataPath)
        print "delDir..."
        os.makedirs(self.rawDataPath)
        ids = self.getIds()
        cookies = self.login()
        i = 1
        for id in ids:
            print i
            url = self.prefixUrl + id
            name = "thread-" + str(i)
            t = threading.Thread(target=self.getProcess,
                                 args=(url, i, cookies,), name=name)
            t.start()
            t.join()
            i += 1

if __name__ == '__main__':
    session = requests.Session()
    cf = ConfigParser.ConfigParser()
    sp = Spider(cf, session, webdriver.Firefox())
    sp.parseConfig()
    sp.getPosts()
