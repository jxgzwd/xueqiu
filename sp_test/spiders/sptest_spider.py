__author__ = 'WD'
import json
import os
import scrapy
from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.shell import inspect_response
from scrapy.contrib.downloadermiddleware import useragent
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from sp_test.items import *

class SptestSpider(CrawlSpider):
    name = 'test'
    allowed_domains = ['xueqiu.com']

    start_urls = [
        'http://xueqiu.com/6327843232'
    ]
    rules = [
        Rule(LinkExtractor(allow=['/\d{10}'], deny=['/\d+/\w+']), 'user_parse')
    ]
    headers = {
        "Host": "xueqiu.com"
        , "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        , "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0"
        , "Accept-Encoding": "gzip,deflate,sdch"
        , "Accept-Language": "zh-CN,zh;q=0.8"
        , "Referer": "http://xueqiu.com/"
    }

    def start_requests(self):
        return [
            FormRequest(
                "http://xueqiu.com/user/login",
                headers=self.headers,# meta={'cookiejar': 1},
                formdata={
                    "username": "jxgzwd@163.com"
                    , "password": "E10ADC3949BA59ABBE56E057F20F883E"
                    , "remember_me": "on"
                    , "areacode": "86"
                },
                callback=self.after_login
            )
        ]

    def after_login(self, response):
        print 'after login'
        filename = 'response_after_login.txt'
        with open(filename, 'wb') as f:
            f.write(response.body)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def user_parse(self, response):
        print 'get page'
        userID = response.url.strip().split('/')[-1]

        jsonStr = response.xpath("//script/text()")[6].extract().split('SNB.profileUser = ')[1]
        userJson = json.loads(jsonStr)
        uItem = self.userBaseJson2Item(userJson)

        jsonStr = response.xpath("//div[@class='status_box ']//script/text()").extract()[1]\
            .split('SNB.data.statuses = ')[1].split(';\n  SNB.data.statusType = ')[0]
        tweetJson = json.loads(jsonStr)
        for j in tweetJson['statuses']:
            tItem = self.tweetJson2Item(j)
            uItem['userTweets'].append(tItem)
            yield tItem

        maxPage = tweetJson['maxPage']
        if maxPage > 1:
            yield Request(response.url+'?page=2', callback=self.user_tweet_parse
                          , meta={'userID': userID, 'uItem': uItem, 'baseURL': response.url}
                          )
        return

    def user_tweet_parse(self, response):
        print 'add page'
        uItem = response.meta['uItem']
        userID = response.meta['userID']
        baseURL = response.meta['baseURL']
        jsStr = response.xpath("//div[@class='status_box ']//script/text()").extract()[1]\
            .split('SNB.data.statuses = ')[1].split(';\n  SNB.data.statusType = ')[0]
        tweetJson = json.loads(jsStr)
        for j in tweetJson['statuses']:
            tItem = self.tweetJson2Item(j)
            uItem['userTweets'].append(tItem)
            yield tItem
        maxPage = tweetJson['maxPage']
        currentPage = tweetJson['page']
        if maxPage > currentPage:
            yield Request(baseURL+'?page=%d' % (currentPage+1), callback=self.user_tweet_parse
                          , meta={'userID': userID, 'uItem': uItem}
                          )
        else:
            yield Request(response.url+'?page=%d' % (currentPage+1), callback=self.user_tweet_parse
                          , meta={'userID': userID, 'uItem': uItem}
                          )
        return

    def user_followers_parse(self, response):
        pass

    def user_attention_parse(self, response):
        pass

    def test_parse(self, response):
        print 'testing'
        filename = 'test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        return

    def user_info_parse(self, response):
        pass

    def user_stock_parse(self, response):
        pass

    def user_group_parse(self, response):
        pass


    def tweetJson2Item(self, tJson):
        tItem = TweetItem()
        tItem['tweetID'] = tJson['id']
        tItem['tweetUserID'] = tJson['user_id']
        tItem['tweetTime'] = tJson['created_at']
        tItem['tweetTitle'] = tJson['title']
        # tItem['tweetText'] = tJson['text']
        tItem['tweetRetweetID'] = tJson['retweet_status_id']
        if tJson['retweet_status_id'] != 0:
            tItem['tweetRetweetUserID'] = tJson['retweeted_status']['user_id']
        else:
            tItem['tweetRetweetUserID'] = 0
        tItem['tweetReplyCount'] = tJson['reply_count']
        tItem['tweetRetweetCount'] = tJson['retweet_count']
        tItem['tweetDonateCount'] = tJson['donate_count']
        tItem['tweetFavCount'] = tJson['fav_count']
        tItem['tweetSource'] = tJson['source']
        return tItem

    def userBaseJson2Item(selfself, uJson):
        uItem = UserItem()
        uItem['userID'] = uJson['id']
        uItem['userName'] = uJson['screen_name']
        uItem['userProfile'] = uJson['profile']
        uItem['userGender'] = uJson['gender']
        uItem['userProvince'] = uJson['province']
        uItem['userDescription'] = uJson['description']
        uItem['userVerified'] = uJson['verified']
        uItem['userVerifiedDescription'] = uJson['verified_description']
        uItem['userTweetsCount'] = uJson['status_count']
        uItem['userFollowersCount'] = uJson['followers_count']
        uItem['userAttentionCount'] = uJson['friends_count']
        uItem['userStocksCount'] = uJson['stocks_count']
        uItem['userTweets'] = []

        uItem['userFollowers'] = []
        uItem['userTopStocks'] = []
        uItem['userDiscussStocks'] = []
        uItem['userAttention'] = []
        uItem['userStocks'] = []
        uItem['userGroupsCount'] = []
        uItem['userGroups'] = []
        return uItem