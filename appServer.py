# -*- coding: utf-8 -*-

from flask import Flask, render_template
from catchutil.DB import *
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/rss")
def rss():
    rss_list = TRssDao.listTRss(True)
    rss_false_list = TRssDao.listTRss(False)
    return render_template("rss.html", rss_list=rss_list, rss_false_list=rss_false_list)


@app.route("/add", methods=['GET', 'POST'])
def add_rss():
    status = {}
    if request.method == 'POST':
        t_rss = TRss(name=request.form["name"], url=request.form["url"])
        if request.form["enabled"]:
            t_rss.enabled = False
        else:
            t_rss.enabled = True
        TRssDao.saveTRss(t_rss)
        status["s"] = "Success"
    return render_template("add_rss.html", status=status)


@app.route("/news")
def read_news():
    rss_items = TRssItemDao.queryTRssItem(**request.args)
    return render_template("news.html", items=rss_items)


@app.route("/items")
def read_items():
    rss_items = TRssItemDao.queryTRssItemByRssId(**request.args)
    return render_template("items.html", items=rss_items, rss_id=request.args["rssId"])


if __name__ == '__main__':
    app.run("0.0.0.0", 8080, True)