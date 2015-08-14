# -*- coding: utf-8 -*-
import feedparser
from bs4 import BeautifulSoup

from DB import *
import datetime
import time
import urllib
import json
import emailUtil
import sched
import socket

socket.setdefaulttimeout(30)

schedule = sched.scheduler(time.time, time.sleep)

"""
根据url获取soup
"""


def get_soup_from_url(url):
    http = urllib.urlopen(url)
    content = http.read()
    soup = BeautifulSoup(content, "html.parser")
    http.close()
    return soup


"""
抓取汽车之家精华帖子
"""


def catch_autohome():
    bbsPrefix = "http://club.autohome.com.cn/bbs/thread-"
    for pageIndex in range(1, 3)[::-1]:
        url = "http://club.autohome.com.cn/ajax/essentialtopics?pageindex=" + str(pageIndex) + "&seriesids=&pagesize=35"
        http = urllib.urlopen(url)
        content = unicode(http.read(), 'GBK')
        obj = json.loads(content)
        articles = obj["data"]
        articles.reverse()
        for article in articles:
            a = bbsPrefix + article["tBBS"] + "-" + str(article["tBBSId"]) + "-" + str(article["topicId"]) + "-1.html"
            if not TRssItemDao.queryTRssItemByLink(a, 2):
                t_rss_item = TRssItem(title=article["tTitle"], link=a, published_date=datetime.datetime.today(),
                                      rss_id=2, created_date=datetime.datetime.today())
                TRssItemDao.saveTRssItem(t_rss_item)
        http.close()


"""
抓取马蜂窝精华游记
"""


def catch_mafengwo():
    urlPrefix = "http://www.mafengwo.cn/ajax/ajax_article.php?start="
    for pageIndex in range(1, 3)[::-1]:
        url = urlPrefix + str(pageIndex)
        soup = get_soup_from_url(url)
        links = soup.select("div dl dt > a")
        links.reverse()
        for a in links:
            tempArray = a["href"].split("\\")
            temp_link = "http://www.mafengwo.cn" + tempArray[2] + tempArray[3]
            if not TRssItemDao.queryTRssItemByLink(temp_link, 3):
                t_rss_item = TRssItem(title=a.text.split("\\r\\n")[0].decode("unicode_escape").strip(), link=temp_link,
                                      published_date=datetime.datetime.today(),
                                      rss_id=3, created_date=datetime.datetime.today())
                TRssItemDao.saveTRssItem(t_rss_item)


"""
抓去雷锋网最新资讯
"""


def catch_leiphone():
    url_prefix = "http://www.leiphone.com/page/"
    for pageIndex in range(1, 2)[::-1]:
        url = url_prefix + str(pageIndex)
        soup = get_soup_from_url(url)
        links = soup.select("li.pbox.clr div.word > a")
        links.reverse()
        for a in links:
            if not TRssItemDao.queryTRssItemByLink(a["href"], 5):
                t_rss_item = TRssItem(title=a.div.string.strip(), link=a["href"],
                                      published_date=datetime.datetime.today(), rss_id=5,
                                      created_date=datetime.datetime.today())
                TRssItemDao.saveTRssItem(t_rss_item)


def catch_logic():
    schedule.enter(60 * 20, 0, catch_logic, ())
    try:
        for rss in TRssDao.listTRss():
            feed = feedparser.parse(rss.url)
            entries = feed.entries
            entries.reverse()
            for entry in entries:
                if rss.id == 4:
                    entry["link"] = entry["link"].split("#")[0]  # 处理v2ex
                if not TRssItemDao.queryTRssItemByLink(entry["link"], rss.id):
                    t_rss_item = TRssItem(title=entry["title"], link=entry["link"], published_date=entry["published"],
                                          rss_id=rss.id, created_date=datetime.datetime.today())
                    TRssItemDao.saveTRssItem(t_rss_item)
        catch_autohome()
        catch_mafengwo()
        #catch_leiphone()
        print("success")
    except Exception, data:
        print(data)
        # 发送邮件
        emailUtil.EmailUtil().send_mail(repr(data))


if __name__ == "__main__":
    schedule.enter(1, 0, catch_logic, ())
    schedule.run()
