# Generated by Django 4.2 on 2023-06-14 08:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0023_alter_notificationchannel_channel_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='channel_room',
            field=models.TextField(default=uuid.UUID('859c8b3d-eba8-4491-9a69-c795297e3044')),
        ),
    ]
