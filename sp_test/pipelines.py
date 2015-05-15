# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class JsonWriterPipeline(object):
    def __init__(self):
        self.filename = open('result\\ttt.j', 'w')

    def process_item(self, item, spider):
        print 'type is'
        print type(item)
        line = json.dumps(dict(item)) + "\n"
        self.filename.write(line)
        return item
