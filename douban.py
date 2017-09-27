# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import random

class DoubanSpider:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5)' +
                                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Referer': 'https://www.douban.com/people/163296676/',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
                        'Cookie': 'FILL IN COOKIE FIELD PLEASE'
                        }
        self.memberlinks = []
        self.flag = False
        self.targetList = []

    def getContacts(self):
        r = requests.get('https://www.douban.com/people/163296676/contacts', headers=self.headers)
        content = r.text
        print(content)
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all("dl", "obu")
        for link in links:
            self.memberlinks.append(link.dd.a["href"])

    def getmemberhomepage(self):
        f = open("member.txt", 'r+', encoding='utf-8')
        count = len(self.memberlinks)
        for i in range(0, count):
            #降低抓取频率
            time.sleep(random.uniform(1.2, 2.0))
            print("Starting to get member's home page for No."+repr(i)+" .URL:"+self.memberlinks[i]+". "+repr(count)+" links in total.")
            r = requests.get(self.memberlinks[i], headers=self.headers)
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            userinfo = soup.find("div", "user-info")
            if userinfo:
                location = userinfo.a
                if location:
                    if location.text.find('上海') != -1:
                        print(location.text)
                        self.targetList.append(self.memberlinks[i])
                        f.write(self.memberlinks[i]+"\n")
                        f.flush()
        f.close()

    def main(self):
        self.getContacts()
        # for link in self.memberlinks:
        #     print(link)
        self.getmemberhomepage()
        for link in self.targetList:
            print(link)


spider = DoubanSpider()
spider.main()