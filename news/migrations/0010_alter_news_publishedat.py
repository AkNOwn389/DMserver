# Generated by Django 4.2 on 2023-05-10 01:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_news_publishedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 10, 1, 5, 43, 592203, tzinfo=datetime.timezone.utc)),
        ),
    ]