# Generated by Django 4.1.7 on 2023-04-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_alter_comment_image_alter_image_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='heigth',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='image',
            name='width',
            field=models.TextField(blank=True),
        ),
    ]
