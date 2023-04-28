# Generated by Django 4.2 on 2023-04-27 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_news_avatar_alter_news_publishedat'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='noOfShare',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 27, 14, 47, 2, 195821, tzinfo=datetime.timezone.utc)),
        ),
    ]
