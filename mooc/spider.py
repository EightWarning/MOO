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
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

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
        self.responseNum = 0
        self.dataPath = ""
        # self.chromeOption = webdriver.ChromeOptions()
        # self.chromeOption.add_argument("--proxy-server=183.131.151.208:80")
        # self.driver = webdriver.Chrome("/usr/bin/chromedriver")
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Chrome(
        #     executable_path="D:\chromedriver\chromedriver.exe")

    # parse config file
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
        self.responseNum = self.cf.getint("page", "responseNum")
        self.dataPath = self.cf.get("data", "dataPath")
        self.dataPath = self.dataPath + self.className + "/"

    # go to right frame and input username and password
    # click login button
    def login(self):
        # self.driver.delete_all_cookies()
        self.driver.maximize_window()
        self.driver.get(self.loginUrl)
        self.driver.switch_to_frame(
            self.driver.find_element_by_tag_name("iframe"))
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
        password.send_keys("10025858iI")
        self.driver.implicitly_wait(30)
        login = self.driver.find_element_by_id(self.loginId).click()
        # return self.driver.get_cookie

    # save content of one page
    # parameters:
    #   pageNum : number of the page
    #   pageContent : content of the page
    # output:
    #   none
    def savePage(self, pageNum, pageContent):
        path = self.dataPath + "page" + str(pageNum)
        os.makedirs(path)
        with open(path + "/page.htm", 'w') as f:
            f.write(pageContent)

    # save content of one post
    # parameters:
    #   pageNum : number of the page
    #   postNum : number of the post
    #   postContent : content of the post
    # output:
    #   none
    def savePost(self, path, resPage, resContent):
        with open(path + "/resPage" + str(resPage) + ".htm", 'w') as f:
            f.write(resContent)

    def calcResPages(self, post):
        onlyBody = SoupStrainer(class_="g-mn1")
        soup = BeautifulSoup(post, "html.parser", parse_only=onlyBody)
        responseNum = int(
            unicode(soup.find("h4", class_="j-reply-info f-fl").string)[1:-2])
        pages = responseNum / self.responseNum
        remainder = responseNum % self.responseNum
        if remainder == 0 and pages == 0:
            return 1
        elif remainder == 0 and pages != 0:
            return pages
        elif remainder != 0:
            return pages + 1

    # click the discussion section
    # parameters:
    #   none
    # output:
    #   none
    def gotoDiscsSection(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_id(self.homeIcon).click()
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_link_text(self.className).click()
        time.sleep(1)
        oldHandle = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if oldHandle != handle:
                self.driver.switch_to_window(handle)
                break
        self.driver.implicitly_wait(30)
        self.driver.find_element_by_link_text(self.targetSection).click()

    # delete exist old files
    # parameters:
    #   path : path of file
    # output:
    #   none
    def delDir(self, path):
        # print path
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            for item in os.listdir(path):
                itemPath = os.path.join(path, item)
                self.delDir(itemPath)
            os.rmdir(path)

    def test(self):
        self.gotoDiscsSection()
        pageNum = self.getPageNum(self.driver.page_source)
        print pageNum
        for pn in xrange(1, pageNum + 1):
            if pn == 1:
                pageContent = self.driver.page_source
                self.savePage(1, pageContent)
            else:
                self.driver.find_element_by_link_text(str(pn)).click()
                time.sleep(3)
                self.savePage(pn, self.driver.page_source)
            href = self.driver.find_elements_by_css_selector(
                self.postCssSelector)

            postNum = len(linkNum) if pn == (pageNum + 1) else self.postNum

            for post in xrange(1, postNum + 1):
                time.sleep(2)
                href[post - 1].click()
                time.sleep(3)
                resContent = self.driver.page_source
                resPages = self.calcResPages(resContent)
                path = self.dataPath + "page" + str(pn) + "/post" + str(post)
                os.makedirs(path)
                if resPages == 1:
                    self.savePost(path, 1, resContent)
                    self.driver.back()
                else:
                    self.savePost(path, 1, resContent)
                    for rp in xrange(2, resPages + 1):
                        self.driver.find_element_by_link_text(str(rp)).click()
                        time.sleep(2)
                        self.savePost(path, rp, self.driver.page_source)
                    self.driver.back()

    # get continue pages of one page
    # parameters:
    #   pageContent : page content
    # output:
    #   pageNum : page number
    def getPageNum(self, pageContent):
        onlyBodyPart = SoupStrainer(class_="u-forumlistwrap j-alltopiclist")
        soup = BeautifulSoup(pageContent, "html.parser",
                             parse_only=onlyBodyPart)
        pageNum = 0
        ll = soup.find_all("a", class_="zpgi")
        for s in ll:
            if s.string != None:
                pageNum += 1
        return pageNum

    def spider(self):
        self.gotoDiscsSection()
        for x in xrange(1, self.pageNum + 1):
            self.driver.find_element_by_link_text(str(x)).click()
            time.sleep(2)
            page = self.driver.page_source
            self.savePage(x, page)
            # print "save page", x
            postNum = 0
            if x == self.pageNum:
                href = self.driver.find_elements_by_css_selector(
                    self.postCssSelector)
                postNum = len(href)
            else:
                postNum = self.postNum
            for p in xrange(1, postNum + 1):
                href = self.driver.find_elements_by_css_selector(
                    self.postCssSelector)
                href[p - 1].click()
                time.sleep(2)
                post = self.driver.page_source
                responsePages = self.calculateResPages(post)
                # print "save post", p
                # print "responsePages", responsePages
                if responsePages == 1:
                    self.savePost(x, p, post)
                    self.driver.back()
                else:
                    path = self.dataPath + "page" + \
                        str(x) + "/post" + str(p)
                    os.makedirs(path)
                    for resPage in xrange(1, responsePages + 1):
                        # print "save resp %d of post %d" % (resPage, p)
                        if resPage == 1:
                            self.savePost2(x, p, resPage, path, post)
                        else:
                            self.driver.find_element_by_link_text(
                                str(resPage)).click()
                            time.sleep(2)
                            self.savePost2(x, p, resPage, path,
                                           self.driver.page_source)
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
    spider.delDir(spider.dataPath)
    spider.login()
    # spider.requestVisit()
    spider.test()

    # spider.spider()

    spider.tearDown()
