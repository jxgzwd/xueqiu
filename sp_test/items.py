# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    userID = scrapy.Field()
    userName = scrapy.Field()
    userProfile = scrapy.Field()
    userGender = scrapy.Field()
    userProvince = scrapy.Field()
    userDescription = scrapy.Field()
    userVerified = scrapy.Field()
    userVerifiedDescription = scrapy.Field()
    userTopStocks = scrapy.Field()      # 经常讨论的股票
    userDiscussStocks = scrapy.Field()  # 能力圈
    userTweetsCount = scrapy.Field()
    userTweets = scrapy.Field()
    userFollowersCount = scrapy.Field()
    userFollowers = scrapy.Field()
    userAttentionCount = scrapy.Field()
    userAttention = scrapy.Field()
    userStocksCount = scrapy.Field()    # 自选股
    userStocks = scrapy.Field()
    userGroupsCount = scrapy.Field()    # 组合
    userGroup = scrapy.Field()


class TweetItem(scrapy.Item):
    tweetID = scrapy.Field()
    tweetUserID = scrapy.Field()
    tweetTime = scrapy.Field()
    tweetTitle = scrapy.Field()
    tweetText = scrapy.Field()
    tweetRetweetID = scrapy.Field()     # 转发自微博ID
    tweetReplyCount = scrapy.Field()
    tweetRetweetCount = scrapy.Field()  # 转发次数
    tweetDonateCount = scrapy.Field()
    tweetFavCount = scrapy.Field()
    tweetSource = scrapy.Field()


class StockItem(scrapy.Item):
    pass


class GroupItem(scrapy.Item):
    pass

