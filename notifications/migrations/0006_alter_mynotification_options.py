# Generated by Django 4.0 on 2023-04-03 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_alter_mynotification_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mynotification',
            options={'ordering': ['seen', '-date']},
        ),
    ]
