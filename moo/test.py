#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import time
import ConfigParser
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

reload(sys)
sys.setdefaultencoding("utf-8")

s = "ssssss"
f = open("data/s/post.htm", 'w')
f.write(s)
f.close()
# with open("data/唐宋词鉴赏/post.htm", 'w') as f:
#     f.write(s)
