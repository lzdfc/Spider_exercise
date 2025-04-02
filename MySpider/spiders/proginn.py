import json
import os
import re
from typing import Iterable
import scrapy
from scrapy import Request
from MySpider.items import MyspiderItem


class ProginnSpider(scrapy.Spider):
    name = "proginn"
    allowed_domains = ["proginn.com"]
    start_urls = ["https://www.proginn.com/cat"]
    page = 1
    headers = {
        "referer": "https://www.proginn.com/"
    }

    # 初始化登录设置
    def start_requests(self) -> Iterable[Request]:
        url = self.start_urls[0]
        tmp = ("PHPSESSID=78l7o8umlbb1f5b4s5cjhp6dp9; user_from_type=%2Findex; "
               "Hm_lvt_c92adf6182a39eb23c24cf43abc3f439=1743574478; HMACCOUNT=F"
               "DAF0B12C3E94A93; client_id=67ecd5d3c2d84; _dx_captcha_vid=B9830"
               "BA8AE3CB755F1D42FE619DEF3035A6A133DBCB602795F3253846585A83B59B8"
               "BE0C3A35392133EF8238162D774FB23650EB68EACDE2AC35982C4258E86D984"
               "B5918E7EA80C9464EAFB810D7FBE1; _dx_uzZo5y=d8750a903f4f947b092b3"
               "7a612300171383a1aebd69cd0e04621749e483ba21b1be291f7; _dx_FMrPY6"
               "=67ecd5ddRbn9pJ7csa7mmTyqGr8LSammse4YHHE1; _dx_app_2db960e4ca0e"
               "aeee12ef63db7e5b3918=67ecd5ddRbn9pJ7csa7mmTyqGr8LSammse4YHHE1; "
               "x_access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI"
               "xMTEzODcxIiwiY3RpbWUiOjE3NDM1NzQ1MTIsImV4cCI6MTc0NjE2NjUxMn0.90"
               "z0L-mke0L4Uc34xFZ-AkeL2hHOC0015M5um2c8JNU; 10000=10000; Hm_lpvt"
               "_c92adf6182a39eb23c24cf43abc3f439=1743575076")

        cookies = {data.split("=")[0]: data.split("=")[1] for data in tmp.split(";")}
        yield Request(url, cookies=cookies, callback=self.first_parse, headers=self.headers)

    # 数据解析
    def parse(self, response):
        cats = response.xpath("//div[@class='item J_user']")
        if cats:
            self.page += 1
            url = self.start_urls[0] + '/page/' + str(self.page)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
        res = {}
        for cat in cats:
            tmp = MyspiderItem()
            tmp['name'] = cat.xpath(".//div[@class='user-info fl']//a/span/text()").get()
            tmp['skills'] = cat.xpath(".//div[@class='user-info fl']//p[@class='desc-item']/span/text()").get()
            tmp['salary'] = cat.xpath(".//div[@class='hire-info fl']//span/text()").get()
            print(tmp)
            yield tmp

    def first_parse(self, response):
        temp = response.xpath("//div[@class='inn-user-filter']/div")

        def initia(facts):
            res = {}
            for fact in facts[1:]:
                rear = re.findall("cat(.*?) ", str(fact))
                rear = rear[0][:-1]
                pre = fact.xpath("./text()").get()
                res[pre] = rear
            return res

        config = {}
        roles = temp[0].xpath(".//a")
        locations = temp[1].xpath(".//a")
        config['roles'] = {}
        config['roles']['全部'] = ""
        config['roles'].update(initia(roles))
        config['locations'] = {}
        config['locations']['全部'] = ""
        config['locations'].update(initia(locations))
        while True:
            print(config['locations'].keys())
            city = input("请输入程序员所在城市(参照上方示例)：")
            if city not in config['locations'].keys():
                os.system("cls")
            else:
                self.start_urls[0] += config['locations'][city]
                break
        os.system("cls")
        while True:
            print(config['roles'].keys())
            role = input("请输入搜索程序员的开发角色(参照上方示例):")
            if role not in config['roles'].keys():
                os.system("cls")
            else:
                self.start_urls[0] += config['roles'][role]
                break
        print(self.start_urls[0])
        yield Request(self.start_urls[0], callback=self.parse)
