# -*- coding: utf-8 -*-
import feedparser

from DB import *
import datetime
import time
import urllib
import json

"""
抓取汽车之家精华帖子
"""


def catch_autohome():
    for pageIndex in range(1, 5):
        bbsPrefix = "http://club.autohome.com.cn/bbs/thread-"
        url = "http://club.autohome.com.cn/ajax/essentialtopics?pageindex=" + str(pageIndex) + "&seriesids=&pagesize=35"
        http = urllib.urlopen(url)
        content = unicode(http.read(), 'GBK')
        obj = json.loads(content)
        for article in obj["data"]:
            a = bbsPrefix + article["tBBS"] + "-" + str(article["tBBSId"]) + "-" + str(article["topicId"]) + "-1.html"
            if not TRssItemDao.queryTRssItemByLink(a, 3):
                t_rss_item = TRssItem(title=article["tTitle"], link=a, published_date=datetime.datetime.today(),
                                      rss_id=3, created_date=str(datetime.datetime.today()))
                TRssItemDao.saveTRssItem(t_rss_item)


if __name__ == "__main__":
    while True:
        for rss in TRssDao.listTRss():
            feed = feedparser.parse(rss.url)
            entries = feed.entries
            entries.reverse()
            for entry in entries:
                if not TRssItemDao.queryTRssItemByLink(entry["link"], rss.id):
                    t_rss_item = TRssItem(title=entry["title"], link=entry["link"], published_date=entry["published"],
                                          rss_id=rss.id, created_date=str(datetime.datetime.today()))
                    TRssItemDao.saveTRssItem(t_rss_item)
        catch_autohome()
        print("success")
        time.sleep(60 * 20)




