# Generated by Django 4.2 on 2023-06-14 08:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0035_alter_notificationchannel_channel_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='channel_room',
            field=models.TextField(default=uuid.UUID('1dcb5433-527f-4e1a-9aa3-d4b62882e7fd')),
        ),
    ]
