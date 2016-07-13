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
soup = BeautifulSoup(open("example"), "html.parser", parse_only=onlyMainTag)
# postContent = soup.find("div", class_="content")

# s = ""
# for x in postContent.stripped_strings:
#     s += x
# print s


print int(
    unicode(soup.find("h4", class_="j-reply-info f-fl").string)[1:-2])
