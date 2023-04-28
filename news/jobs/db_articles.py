from news.models import News
from news.serializers import NewsSerializers



def createNewsAticles(
        avatar:str,
        title:str,
        news_id:str,
        name:str,
        author:str,
        description:str,
        url:str,
        urlToImage:str,
        publishedAt:str,
        content:str) -> News:
    return News.objects.create(
        avatar = avatar,
        title = title,
        news_id = news_id,
        name = name,
        author = author,
        description = description,
        url = url,
        urlToImage = urlToImage,
        publishedAt = publishedAt,
        content = content
        )
