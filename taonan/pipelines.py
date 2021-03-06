# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class TaonanPipeline(object):

    def __init__(self):
        self.filename = open('taonan.json','wb')


    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.filename.write(content.encode())
        return item

    def close_spider(self,spider):
        self.filename.close()
