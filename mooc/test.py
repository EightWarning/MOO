#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import jieba
import ConfigParser
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import jieba.posseg as pseg

reload(sys)
sys.setdefaultencoding("utf-8")


def requestVisit(self):
    self.gotoDiscsSection()
    headers = {"Host": "www.icourse163.org",
               "Connection": "keep-alive",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5",
               "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}
    s = requests.session()
    s.headers.update(headers)
    for cookie in self.driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)

    url = "http://www.icourse163.org/learn/hit-1001578001?tid=1001652002#/learn/forumdetail?pid=1002472093"
    response = s.get(url)
    print response.text
    print response.url


def test():


if __name__ == '__main__':
    test()
