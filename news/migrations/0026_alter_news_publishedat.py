# Generated by Django 4.2 on 2023-06-14 08:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0025_alter_news_publishedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 8, 16, 59, 871145, tzinfo=datetime.timezone.utc)),
        ),
    ]
