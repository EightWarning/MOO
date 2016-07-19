#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

loginUrl = 'http://www.xuetangx.com/v2/login_ajax'
destUrl = 'http://www.xuetangx.com/courses/TsinghuaX/TSINGHUA101/_/discussion/forum?ajax=1&page=1&sort_key=date&sort_order=desc'
primUrl = 'http://www.xuetangx.com/courses/TsinghuaX/TSINGHUA101/_/discussion/forum/i4x-edx-templates-course-Empty/threads/'
formatUrl = "http://www.xuetangx.com/courses/TsinghuaX/TSINGHUA101/_/discussion/forum?ajax=1&page=%d&sort_key=date&sort_order=desc"
username = 'cbpy'
password = '10025858iIA'
data = {
    'username': username,
    'password': password,
    'remember': 'true',
    'csrfmiddlewaretoken': 'KmTpCJEGFhAIqx9euxH3pperZ9ynAsAm'
}
headers = {
    'Host': 'www.xuetangx.com',
    'Origin': 'http://www.xuetangx.com',
    'Referer': 'http://www.xuetangx.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
    'X-CSRFToken': 'KmTpCJEGFhAIqx9euxH3pperZ9ynAsAm',
    'X-Requested-With': 'XMLHttpRequest'
}
proxies = {"https": "http://41.118.132.69:4433"}


class Spider(object):
    """docstring for ClassName"""

    def __init__(self, session):
        self.loginUrl = loginUrl
        self.destUrl = destUrl
        self.primUrl = primUrl
        self.data = data
        self.headers = headers
        self.formatUrl = formatUrl
        self.proxies = proxies
        self.session = session

    def login(self):
        try:
            res = self.session.post(
                self.loginUrl, data=self.data, headers=self.headers, proxies=self.proxies)
            return res.cookies
        except Exception, e:
            print "login() post error, ", e
        return None

    def getIds(self):
        cookies = self.login()
        if cookies:
            try:
                response = self.session.get(
                    self.destUrl, cookies=cookies, headers=self.headers)
            except Exception, e:
                print "getIds() get error, ", e
            content = response.content
            # print content
            pagesNum = re.compile('''"num_pages": (\w+?)''')
            pages = pagesNum.findall(content)
            pages = pages[0]
            pages = int(pages)
            pattern = re.compile('''"id": "(.+?)"''')
            ids = []
            i = 1
            while i <= pages:
                url = formatUrl % i
                try:
                    response = self.session.get(
                        url, cookies=cookies, headers=self.headers)
                except Exception, e:
                    print "getIds() get error, ", e
                content = response.content
                tmp = pattern.findall(content)
                print i
                print tmp
                ids.extend(tmp)
                i = i + 1
            return ids, cookies
        return None, None

    def getPosts(self):
        ids, cookies = self.getIds()
        if ids and cookies:
            try:
                f = open('/home/hadoop/mooc/data/test/test.data', 'w')
            except Exception, e:
                print "getPosts() open file error, ", e
            for item in ids:
                url = self.primUrl + item
                try:
                    response = self.session.get(
                        url, cookies=cookies, headers=headers)
                except Exception, e:
                    print "getPosts() get error, ", e
                patternBody = re.compile('''"body": "(.+?)"''')
                bodys = patternBody.findall(response.content)
                # print type(bodys)
                # print bodys
                for post in bodys:
                    post = post.replace('\\n', '')
                    post = post.decode("unicode_escape")
                    print post
                    f.write(post)
                    f.write('\n')
            return True
        return False


def test():
    session = requests.Session()
    sp = Spider(session)
    if sp.getPosts():
        print 'ok'
    else:
        print 'not ok'


if __name__ == '__main__':
    test()
