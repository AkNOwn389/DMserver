# Generated by Django 4.2 on 2023-04-27 10:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True)),
                ('news_id', models.TextField(blank=True)),
                ('name', models.TextField(blank=True)),
                ('author', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField()),
                ('urlToImage', models.URLField(blank=True)),
                ('publishedAt', models.DateTimeField(default=datetime.datetime(2023, 4, 27, 10, 6, 59, 154380))),
                ('content', models.TextField(blank=True)),
            ],
        ),
    ]