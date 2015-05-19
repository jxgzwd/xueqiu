# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from sp_test.items import *

class JsonWriterPipeline(object):
    def __init__(self):
        self.tweetfile = open('result'+os.sep+'tweet.jsons', 'w')
        self.userfile = open('result'+os.sep+'user.jsons', 'w')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"

        if type(item) == type(TweetItem()):
            self.tweetfile.write(line)

        if type(item) == type(UserItem()):
            self.userfile.write(line)

        return item
