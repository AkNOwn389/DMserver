# Generated by Django 4.2 on 2023-04-27 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='noOfComment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='news',
            name='noOfLike',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='news',
            name='publishedAt',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 27, 10, 40, 56, 662616)),
        ),
    ]
