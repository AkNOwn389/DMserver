# Generated by Django 4.2 on 2023-04-27 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_noofcomment_news_nooflike_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 27, 12, 13, 13, 970505)),
        ),
    ]
