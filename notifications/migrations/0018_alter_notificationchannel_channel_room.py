# Generated by Django 4.2 on 2023-06-14 08:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0017_alter_notificationchannel_channel_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='channel_room',
            field=models.TextField(default=uuid.UUID('47435468-0710-4dda-9410-1d2f1e7850fc')),
        ),
    ]
