# Generated by Django 4.0 on 2023-03-12 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0010_alter_chatmessage_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='created_time',
            field=models.TimeField(default='3:49:15.593120'),
        ),
    ]