# -*- coding: utf-8 -*-
import feedparser
from bs4 import BeautifulSoup

from DB import *
import datetime
import time
import urllib
import json

"""
抓取汽车之家精华帖子
"""


def catch_autohome():
    bbsPrefix = "http://club.autohome.com.cn/bbs/thread-"
    for pageIndex in range(1, 6)[::-1]:
        url = "http://club.autohome.com.cn/ajax/essentialtopics?pageindex=" + str(pageIndex) + "&seriesids=&pagesize=35"
        http = urllib.urlopen(url)
        content = unicode(http.read(), 'GBK')
        obj = json.loads(content)
        articles = obj["data"]
        articles.reverse()
        for article in articles:
            a = bbsPrefix + article["tBBS"] + "-" + str(article["tBBSId"]) + "-" + str(article["topicId"]) + "-1.html"
            if not TRssItemDao.queryTRssItemByLink(a, 3):
                t_rss_item = TRssItem(title=article["tTitle"], link=a, published_date=datetime.datetime.today(),
                                      rss_id=3, created_date=datetime.datetime.today())
                TRssItemDao.saveTRssItem(t_rss_item)

"""
抓取马蜂窝最新游记
"""

def catch_mafengwo():
    urlPrefix = "http://www.mafengwo.cn/ajax/ajax_article.php?type=1&start="
    for pageIndex in range(1, 6)[::-1]:
        url = urlPrefix + str(pageIndex)
        http = urllib.urlopen(url)
        content = http.read()
        soup = BeautifulSoup(content, "lxml")
        links = soup.select("div dl dt > a")
        links.reverse()
        for a in links:
            tempArray = a["href"].split("\\")
            temp_link = "http://www.mafengwo.cn" + tempArray[2] + tempArray[3]
            if not TRssItemDao.queryTRssItemByLink(temp_link, 4):
                t_rss_item = TRssItem(title=a.text.split("\\r\\n")[0].decode("unicode_escape").strip(), link=temp_link, published_date=datetime.datetime.today(),
                                      rss_id=4, created_date=datetime.datetime.today())
                TRssItemDao.saveTRssItem(t_rss_item)
        http.close()


if __name__ == "__main__":
    while True:
        for rss in TRssDao.listTRss():
            feed = feedparser.parse(rss.url)
            entries = feed.entries
            entries.reverse()
            for entry in entries:
                if not TRssItemDao.queryTRssItemByLink(entry["link"], rss.id):
                    t_rss_item = TRssItem(title=entry["title"], link=entry["link"], published_date=entry["published"],
                                          rss_id=rss.id, created_date=datetime.datetime.today())
                    TRssItemDao.saveTRssItem(t_rss_item)
        catch_autohome()
        catch_mafengwo()
        print("success")
        time.sleep(60 * 20)




