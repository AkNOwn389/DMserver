# Generated by Django 4.2 on 2023-05-10 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_delete_likecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='isDeleted',
            field=models.BooleanField(default=False),
        ),
    ]
