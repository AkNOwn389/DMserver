from datetime import datetime, time, date, timedelta
from newsapi import NewsApiClient
from django.conf import settings
from news.models import News
import json
import newsapi
from .db_articles import createNewsAticles
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import random
session = requests.Session()


def start():
    print("Running get new before schedule")
    getNews()
    scheduler = BackgroundScheduler()
    scheduler.add_job(getNews, 'interval', seconds = 7200)
    scheduler.start()

def getNews():
    cnn_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682605042/media/Martz90-Circle-Addon1-Cnn.512_cjj7cw.png"
    bbc_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682605042/media/Martz90-Circle-Bbc-news.512_o51tko.png"
    firefox_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682605042/media/Dakirby309-Windows-8-Metro-Web-Fox-News-Metro.256_brevbz.png"
    polygon_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632098/media/gpZKXbHG_400x400_drfpuf.jpg"
    abc_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632097/media/3flU1i5o_400x400_xpzvge.jpg"
    google_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632097/media/NWRtL2J__400x400_tnyogv.jpg"
    nasa_avatar = "https://res.cloudinary.com/dlcgldmau/image/upload/v1682632098/media/0ZxKlEKB_400x400_zih4au.jpg"


    src = ["cnn-philippines", "bbc-news", "cnn", "abc-news", "google-news", "polygon"]
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
                print(jsonData)
            except KeyError:
                print(f"Exception: {jsonData['message']}")
                break
            if jsonData['articles'] == []:
                break
            for i in jsonData['articles']:
                go = True
                for x in all_news:
                    if i['content'] == x.content or i['description'] == x.description or i['title'] == x.title:
                        go = False
                if go == True:
                    title = i['title']
                    news_id = i['source']['id']
                    name = i['source']['name']
                    author = i['author']
                    urlToImage = i['urlToImage']
                    if author == None:
                        author = ""
                    if urlToImage == None or urlToImage == "":
                        continue
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
                    elif news_id == "cnn-philippines":
                        avatar = cnn_avatar
                    elif news_id == "NASA":
                        avatar = nasa_avatar
                    try:
                        description = i['description']
                    except:
                        description = ""
                    try:
                        url = i['url']
                    except:
                        url = ""

                    publishedAt = i['publishedAt']
                    try:
                        content = i['content']
                    except:
                        content = ""
                    news = createNewsAticles(
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







