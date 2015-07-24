# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, create_engine, INTEGER, BOOLEAN
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:////Users/lingfeizhang/IdeaProjects/pythontest/catch_feed/db/db.sqlite' ) #echo=True
DBSession = sessionmaker(bind=engine)


class TRss(Base):
    __tablename__ = 't_rss'

    id = Column(INTEGER(), primary_key=True)
    name = Column(String())
    url = Column(String())
    enabled = Column(BOOLEAN())


class TRssItem(Base):
    __tablename__ = "t_rss_item"
    id = Column(INTEGER(), primary_key=True)
    rss_id = Column(INTEGER())
    title = Column(String())
    link = Column(String())
    published_date = Column(String())
    created_date = Column(String())


class TRssDao:
    @staticmethod
    def saveTRss(t_rss):
        session = DBSession()
        session.add(t_rss)
        session.commit()
        session.close()

    @staticmethod
    def listTRss(enabled=True):
        session = DBSession()
        result = session.query(TRss).filter(TRss.enabled == enabled).all()
        session.close()
        return result


class TRssItemDao:
    @staticmethod
    def saveTRssItem(t_rss_item):
        session = DBSession()
        session.add(t_rss_item)
        session.commit()
        session.close()

    @staticmethod
    def queryTRssItemByLink(link):
        session = DBSession()
        result = session.query(TRssItem).filter(TRssItem.link == link).first()
        session.close()
        return result

    @staticmethod
    def queryTRssItem(**kwargs):
        result = []
        session = DBSession()
        query = session.query(TRssItem)
        if kwargs.get("itemId", None):
            if kwargs.get("prev", None) != None:
                query = query.filter(TRssItem.id > int(kwargs["itemId"][0]))
                query = query.order_by(TRssItem.id.asc())
                query=query.offset(0)
                query=query.limit(35)
                result = query.all()
                result.reverse()
            if kwargs.get("next", None) != None:
                query = query.filter(TRssItem.id < int(kwargs["itemId"][0]))
                query = query.order_by(TRssItem.id.desc())
                query=query.offset(0)
                query=query.limit(35)
                result = query.all()
        else:
            result = query.order_by(TRssItem.id.desc()).offset(0).limit(35).all()

        session.close()
        return result
