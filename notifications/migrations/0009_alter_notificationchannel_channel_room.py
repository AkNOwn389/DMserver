# Generated by Django 4.2 on 2023-06-14 08:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_alter_notificationchannel_channel_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='channel_room',
            field=models.TextField(default=uuid.UUID('7f673208-8578-4ffb-afaf-2f051986ae6a')),
        ),
    ]
