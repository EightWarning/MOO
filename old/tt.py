# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

url = "http://www.icourse163.org"
driver = webdriver.Firefox()
driver.get(url)
