# Generated by Django 4.2 on 2023-06-14 08:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0011_alter_notificationchannel_channel_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='channel_room',
            field=models.TextField(default=uuid.UUID('bc79bb6b-0ba8-4982-b356-2957f3eba0c0')),
        ),
    ]