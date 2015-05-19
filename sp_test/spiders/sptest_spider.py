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
        #inspect_response(response, self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def user_parse(self, response):
        print 'get page'
        jsonStr = response.xpath("//script/text()")[6].extract().split('SNB.profileUser = ')[1]
        userJson = json.loads(jsonStr)
        json.dump(userJson, open('user.json', 'w'))
        userID = response.url.strip().split('/')[-1]
        jsonStr = response.xpath("//div[@class='status_box ']//script/text()").extract()[1].split('SNB.data.statuses = ')[1]\
            .split(';\n  SNB.data.statusType = ')[0]
        tweetJson = json.loads(jsonStr)
        maxPage = tweetJson['maxPage']
        print '**************************'
        print userID
        print maxPage
        for j in tweetJson['statuses']:
            tItem = self.tweetJson2Item(j)
            yield tItem
        for page in range(2, maxPage+1):
            print response.url+'?page=%d' % page
            yield Request(response.url+'?page=%d' % page, callback=self.user_tweet_parse
                          , meta={'userID': userID}
                          )

        # yield Request(
        #         'http://xueqiu.com/friendships/groups/members.json?page=1&uid=1956603092&gid=0&_=1431075883261'
        #         , callback=self.test_parse
        #         , headers=self.headers
        # )

        filename = 'result'+os.sep+userID + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        return

    def user_tweet_parse(self, response):
        print 'add page'
        userID = response.meta['userID']
        jsStr = response.xpath("//div[@class='status_box ']//script/text()").extract()[1]
        jsStr = jsStr.split('SNB.data.statuses = ')[1]
        jsStr = jsStr.split(';\n  SNB.data.statusType = ')[0]
        tmpJson = json.loads(jsStr)
        f = open('result'+os.sep+userID+'_%d.json' % tmpJson['page'], 'w')
        json.dump(tmpJson, f)
        f.close()
        return

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
        tItem['tweetReplyCount'] = tJson['reply_count']
        tItem['tweetRetweetCount'] = tJson['retweet_count']
        tItem['tweetDonateCount'] = tJson['donate_count']
        tItem['tweetFavCount'] = tJson['fav_count']
        tItem['tweetSource'] = tJson['source']
        return tItem

    def userJson2Item(selfself, uJson):
        uItem = UserItem()
        uItem['userID'] = uJson['id']
        uItem['userName'] = uJson['screen_name']
        uItem['userProfile'] = uJson['profile']
        uItem['userGender'] = uJson['gender']
        uItem['userProvince'] = uJson['province']
        uItem['userDescription'] = uJson['description']
        uItem['userVerified'] = uJson['verified']
        uItem['userVerifiedDescription'] = uJson['verified_description']
        uItem['userTopStocks'] = uJson['id']
        uItem['userDiscussStocks'] = uJson['id']
        uItem['userTweetsCount'] = uJson['status_count']
        uItem['userTweets'] = uJson['id']
        uItem['userFollowersCount'] = uJson['followers_count']
        uItem['userFollowers'] = uJson['id']
        uItem['userAttentionCount'] = uJson['id']
        uItem['userAttention'] = uJson['id']
        uItem['userStocksCount'] = uJson['stocks_count']
        uItem['userStocks'] = uJson['id']
        uItem['userGroupsCount'] = uJson['id']
        uItem['userGroup'] = uJson['id']