# Generated by Django 4.2 on 2023-10-12 08:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0053_alter_news_publishedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 12, 8, 30, 34, 644934, tzinfo=datetime.timezone.utc)),
        ),
    ]