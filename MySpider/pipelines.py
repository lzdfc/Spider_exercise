# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import date

from openpyxl import Workbook

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyspiderPipeline:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["名字", "技能", "工资"])

    def process_item(self, item, spider):
        self.ws.append([item['name'], item['skills'], item['salary']])
        return item

    def close_spider(self, spider):
        self.wb.save(filename=f'SearchResult{date.today()}.xlsx')
