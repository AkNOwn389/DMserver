# Generated by Django 4.2 on 2023-05-09 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_likepost_reactiontype'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LikeComment',
        ),
    ]