#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import subprocess
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
s1 = "ls"
s2 = "-l"
child = subprocess.Popen([s1, s2], stdout=subprocess.PIPE)
out = child.communicate()
print out
