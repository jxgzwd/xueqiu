# -*- coding: utf-8 -*-

# Scrapy settings for sp_test project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sp_test'

SPIDER_MODULES = ['sp_test.spiders']
NEWSPIDER_MODULE = 'sp_test.spiders'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'sp_test.spiders.random_useragent.RandomUserAgentMiddleware': 400
}
ITEM_PIPELINES = {
    'sp_test.pipelines.JsonWriterPipeline': 300
}
DOWNLOAD_DELAY = 0.25
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'sp_test (+http://www.yourdomain.com)'
