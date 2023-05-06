from datetime import datetime, timedelta
from .db_articles import createNewsAticles
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup as soup
from newsapi import NewsApiClient
from django.conf import settings
from news.models import News
import json
import newsapi
import requests
import random
import time
session = requests.Session()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getNews, 'interval', seconds = 28000)
    scheduler.start()
    NewsUpdater()
    NewsRemover()


class NewsUpdater():
    def __init__(self) -> None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.start, "interval", seconds = 3600)
        scheduler.start()

    cnn_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682605042/media/Martz90-Circle-Addon1-Cnn.512_cjj7cw.png"
    bbc_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682605042/media/Martz90-Circle-Bbc-news.512_o51tko.png"
    firefox_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682605042/media/Dakirby309-Windows-8-Metro-Web-Fox-News-Metro.256_brevbz.png"
    polygon_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632098/media/gpZKXbHG_400x400_drfpuf.jpg"
    abc_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632097/media/3flU1i5o_400x400_xpzvge.jpg"
    google_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632097/media/NWRtL2J__400x400_tnyogv.jpg"
    nasa_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632098/media/0ZxKlEKB_400x400_zih4au.jpg"
    no_id_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682755920/media/news_fk8vqm.png"
    def saveInDataBase(self):
        db = createNewsAticles(
            avatar = self.avatar,
            title = self.title,
            news_id = self.news_id,
            name = self.name,
            author = self.author,
            description = self.description,
            url = self.url,
            urlToImage = self.urlToImage,
            publishedAt = self.publishedAt,
            content = self.content)
        print(f"new news update: {db}")

    def filterNews(self, oldNews, newNews:list[dict]) -> list[dict]:
        for i in oldNews:
            i:News = i
            for x in newNews:
                if i.content == x['content']:
                    newNews.remove(x)
                elif i.title == x['title']:
                    newNews.remove(x)
                elif i.description == x['description']:
                    newNews.remove(x)
        self.hasNewNews = True if len(newNews) > 0 else False
        return newNews
    def getNewsAvatar(self):
        news_id = self.news_id
        if news_id == "bbc-news":
            self.avatar = self.bbc_avatar
            return
        elif news_id == "cnn":
            self.avatar = self.cnn_avatar
            return
        elif news_id == "abc-news":
            self.avatar = self.abc_avatar
            return
        elif news_id == "google-news":
            self.avatar = self.google_avatar
            return
        elif news_id == "polygon":
            self.avatar = self.polygon_avatar
            return
        elif news_id == "cnn-ph":
            self.avatar = self.cnn_avatar
            return
        elif news_id == "NASA":
            self.avatar = self.nasa_avatar
            return
        elif news_id == None or news_id == "":
           self.avatar = self.no_id_avatar
           return
        else:
            self.avatar = self.no_id_avatar
            return

    def inpuTValue(self, news_):
        for i in news_:
            self.title = "" if i['title'] == None else i['title']
            self.publishedAt = i['publishedAt']
            self.news_id = "" if i['source']['id'] == None else i['source']['id']
            self.name = "" if i['source']['name'] == None else i['source']['name']
            self.author = "" if i['author'] == None else i['author']
            self.urlToImage = "" if i['urlToImage'] == None else i['urlToImage']
            self.description = "" if i['description'] == None else i['description']
            self.url = "" if i['url'] == None else i['url']
            self.content = "" if i['content'] == None else i['content']
            self.getNewsAvatar()

    def start(self):
        key = settings.NEWS_API_KEY
        key2 = settings.NEWS_API_KEY2
        country_list = ['us', 'ph']
        pageSize = 30
        page_start = 1
        print("updating news")
        for country in country_list:
            page = page_start
            news_url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={key}"
            response = session.get(url=news_url)
            json_response = json.loads(response.text)
            #print(json_response)
            if "articles" not in json_response:
                break
            all_news = News.objects.all()
            news_ = self.filterNews(all_news, json_response['articles'])
            if not self.hasNewNews:
                break
            else:
                self.inpuTValue(news_=news_)
                self.saveInDataBase()


def getNews():
    cnn_avatar = "https://res.cloudinary.com/dkjejhexm/image/upload/v1683230298/Martz90-Circle-Addon1-Cnn.512_qutkgy.png"
    bbc_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682605042/media/Martz90-Circle-Bbc-news.512_o51tko.png"
    firefox_avatar = "https://res.cloudinary.com/dkjejhexm/image/upload/v1683230298/Dakirby309-Windows-8-Metro-Web-Fox-News-Metro.256_gwrziw.png"
    polygon_avatar = "https://res.cloudinary.com/dkjejhexm/image/upload/v1683230287/gpZKXbHG_400x400_l6xwsl.jpg"
    abc_avatar = "https://res.cloudinary.com/dkjejhexm/image/upload/v1683230287/3flU1i5o_400x400_ibnsbe.jpg"
    google_avatar = "https://res.cloudinary.com/dkjejhexm/image/upload/v1683230286/NWRtL2J__400x400_bivtae.jpg"
    nasa_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632098/media/0ZxKlEKB_400x400_zih4au.jpg"
    no_id_avatar = "https://res.cloudinary.com/dkjejhexm/image/upload/v1683230287/news_abewli.png"


    src = ["cnn-ph", "bbc-news", "cnn", "abc-news", "google-news", "polygon"]
    page = 1
    pagesize = 30
    key = settings.NEWS_API_KEY
    key2 = settings.NEWS_API_KEY2
    sortby = "popularity"
    date_now = datetime.now()
    day_7_from_now = date_now - timedelta(days=7)
    for news_source in src:
        page = 1
        while True:
            #source = random.choice(src)
            print("Updating news articles")
            res = session.get(f"https://newsapi.org/v2/everything?sortBy={sortby}&apiKey={key2}&pageSize={pagesize}&page={page}&sources={news_source}")
            jsonData = json.loads(res.text.encode('utf-8').decode())
            all_news = News.objects.all()
            page = page +1
            try:
                print(jsonData['source']['id'])
            except:
                pass
            try:
                jsonData['articles']
            except KeyError:
                print(f"Exception: {jsonData['message']}")
                break
            if jsonData['articles'] == []:
                break
            for i in jsonData['articles']:
                go = True
                for x in all_news:
                    if i['content'] == x.content:
                        go = False
                if go == True:
                    title = "" if i['title'] == None else i['title']
                    publishedAt = i['publishedAt']
                    news_id = "" if i['source']['id'] == None else i['source']['id']
                    name = "" if i['source']['name'] == None else i['source']['name']
                    author = "" if i['author'] == None else i['author']
                    urlToImage = "" if i['urlToImage'] == None else i['urlToImage']
                    description = "" if i['description'] == None else i['description']
                    url = "" if i['url'] == None else i['url']
                    content = "" if i['content'] == None else i['content']

                    #news avatar
                    if news_id == "bbc-news":
                        avatar = bbc_avatar
                    elif news_id == "cnn":
                        avatar = cnn_avatar
                    elif news_id == "abc-news":
                        avatar = abc_avatar
                    elif news_id == "google-news":
                        avatar = google_avatar
                    elif news_id == "polygon":
                        avatar = polygon_avatar
                    elif news_id == "cnn-ph":
                        avatar = cnn_avatar
                    elif news_id == "NASA":
                        avatar = nasa_avatar
                    elif news_id == None or news_id == "":
                        no_id_avatar
                    else:
                        no_id_avatar

                    createNewsAticles(
                        avatar = avatar,
                        title = title,
                        news_id = news_id,
                        name = name,
                        author = author,
                        description = description,
                        url = url,
                        urlToImage = urlToImage,
                        publishedAt = publishedAt,
                        content = content)



class NewsRemover:
    def __init__(self) -> None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.start, "interval", seconds = 7200, max_instances=1)
        scheduler.start()



    def start(self):
        news_all = News.objects.all()
        for i in news_all:
            try:
                response = session.get(i.url)
            except:
                continue
            if response.status_code == 400:
                print(f"Broken news url with status code:{response.status_code} deleting: {i}")
                i.delete()



