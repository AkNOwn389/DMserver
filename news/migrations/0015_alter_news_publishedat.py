# Generated by Django 4.2 on 2023-05-14 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_rename_noofcomment_news_noofcomment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 14, 16, 4, 27, 679178, tzinfo=datetime.timezone.utc)),
        ),
    ]
