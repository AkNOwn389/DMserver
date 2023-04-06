# Generated by Django 4.1.7 on 2023-04-03 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_options_post_privacy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.CharField(choices=[('1', 'Public'), ('2', 'Friends'), ('3', 'Private')], default='1', max_length=2),
        ),
    ]