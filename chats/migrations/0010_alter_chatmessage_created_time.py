# Generated by Django 4.0 on 2023-03-12 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0009_alter_chatmessage_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='created_time',
            field=models.TimeField(default='3:46:55.790773'),
        ),
    ]