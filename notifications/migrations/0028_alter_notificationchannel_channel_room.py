# Generated by Django 4.2 on 2023-06-14 08:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0027_alter_notificationchannel_channel_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='channel_room',
            field=models.TextField(default=uuid.UUID('0b6a863e-4db9-4c13-87b9-177624d3ab74')),
        ),
    ]
