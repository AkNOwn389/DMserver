# Generated by Django 4.2 on 2023-05-14 16:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_alter_news_publishedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 14, 16, 30, 0, 513753, tzinfo=datetime.timezone.utc)),
        ),
    ]
