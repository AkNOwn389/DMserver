# Generated by Django 4.2 on 2023-05-05 00:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_news_id_alter_news_publishedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 5, 0, 7, 21, 644629, tzinfo=datetime.timezone.utc)),
        ),
    ]
