# Generated by Django 4.2 on 2023-06-14 08:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0031_alter_notificationchannel_channel_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationchannel',
            name='channel_room',
            field=models.TextField(default=uuid.UUID('d34c4fe2-259e-41c8-bc79-00f445bc36fc')),
        ),
    ]
