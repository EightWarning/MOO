# -*- coding: utf-8 -*-
import ConfigParser
import time
import requests
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
loginUrl = "http://www.icourse163.org/member/login.htm#/login"
url = "http://www.icourse163.org/learn/cau-1001614009?tid=1001691005#/learn/forumindex"

# chromeOption = webdriver.ChromeOptions()
# chromeOption.add_argument("--proxy-server=110.230.165.217:81")

driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get(loginUrl)
time.sleep(2)
driver.switch_to_frame(0)

# driver.find_element_by_css_selector(
#     "div.tab2").click()

# driver.find_element_by_xpath(
#     '//div[@class="tab tab2 f-pr j-tabs f-fl f-f0 inactive"]').click()
# time.sleep(2)
try:
    username = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
except Exception, e:
    raise e
try:
    password = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
except Exception, e:
    raise e
username.send_keys("cbbupt@163.com")
password.send_keys("10025858iI")
driver.implicitly_wait(30)
driver.find_element_by_id("dologin").click()
