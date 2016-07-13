# -*- coding: utf-8 -*-
import os
import time
import requests
import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Spider(object):
    """docstring for Spider"""

    def __init__(self, cf):
        super(Spider, self).__init__()
        self.cf = cf
        self.loginUrl = ""
        self.baseUrl = ""
        self.username = ""
        self.password = ""
        self.className = ""
        self.targetSection = ""
        self.postCssSelector = ""
        self.email = ""
        self.password = ""
        self.loginId = ""
        self.homeIcon = ""
        self.pageNum = 0
        self.postNum = 0
        # self.chromeOption = webdriver.ChromeOptions()
        # self.chromeOption.add_argument("--proxy-server=183.131.151.208:80")
        self.driver = webdriver.Chrome("/usr/bin/chromedriver")
        # self.driver = webdriver.Firefox()

    def parseConf(self):
        self.cf.read("conf.cfg")
        self.loginUrl = self.cf.get("url", "loginUrl")
        self.baseUrl = self.cf.get("url", "baseUrl")
        self.username = self.cf.get("account", "username")
        self.password = self.cf.get("account", "password")
        self.className = self.cf.get("classInfo", "className")
        self.targetSection = self.cf.get("classInfo", "targetSection")
        self.postCssSelector = self.cf.get("classInfo", "postCssSelector")
        self.email = self.cf.get("moocLogin", "email")
        self.password = self.cf.get("moocLogin", "password")
        self.loginId = self.cf.get("moocLogin", "loginId")
        self.homeIcon = self.cf.get("moocLogin", "homeIcon")
        self.pageNum = self.cf.getint("page", "pageNum")
        self.postNum = self.cf.getint("page", "postNum")

    '''
    login on the home page
    '''

    def login(self):
        # self.driver.delete_all_cookies()
        self.driver.maximize_window()
        self.driver.get(self.loginUrl)
        self.driver.switch_to_frame(0)
        try:
            username = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.NAME, self.email))
            )
        except Exception, e:
            print e
            raise e
        username.send_keys(self.username)
        try:
            password = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.NAME, self.password))
            )
        except Exception, e:
            print e
            raise e
        password.send_keys("xxxxxxxx")
        self.driver.implicitly_wait(30)
        login = self.driver.find_element_by_id(self.loginId).click()
        # return self.driver.get_cookie

    def savePage(self, x, page):
        path = "data/page" + str(x)
        if os.path.exists(path):
            for f in os.listdir(path):
                os.remove(path + "/" + f)
        else:
            os.makedirs(path)
        f = open(path + "/page.htm", 'w')
        f.write(page)
        f.close()

    def savePost(self, x, p, post):
        path = "data/page" + str(x)
        f = open(path + "/post" + str(p) + ".htm", 'w')
        f.write(post)
        f.close()

    def getResponsePages(self, pageSource):
    '''
    get the pages and posts
    '''

    def spider(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(self.homeIcon).click()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_link_text(self.className).click()
        time.sleep(3)
        oldHandle = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if oldHandle != handle:
                self.driver.switch_to_window(handle)
                break
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_link_text(self.targetSection).click()
        for x in xrange(1, self.pageNum + 1):
            self.driver.find_element_by_link_text(str(x)).click()
            time.sleep(2)
            # self.driver.implicitly_wait(30)
            page = self.driver.page_source
            self.savePage(x, page)
            postNum = 0
            if x == self.pageNum:
                href = self.driver.find_elements_by_css_selector(
                    self.postCssSelector)
                postNum = len(href)
            else:
                postNum = self.postNum
            for p in xrange(0, postNum):
                href = self.driver.find_elements_by_css_selector(
                    self.postCssSelector)
                href[p].click()
                time.sleep(2)
                # self.driver.implicitly_wait(30)
                post = self.driver.page_source
                self.savePost(x, p + 1, post)
                self.driver.back()

    '''
    close the driver
    '''

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    spider = Spider(cf)
    spider.parseConf()
    spider.login()
    spider.spider()

    spider.tearDown()
