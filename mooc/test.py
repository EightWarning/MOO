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

onlyMainTag = SoupStrainer(class_="g-mn1")
soup = BeautifulSoup(open("example"), "lxml", parse_only=onlyMainTag)
postContent = soup.find("div", class_="content")
print postContent
s = ""
for x in postContent.stripped_strings:
    s += x
print s
