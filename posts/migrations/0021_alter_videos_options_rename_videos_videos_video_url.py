# Generated by Django 4.2 on 2023-04-09 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0020_alter_image_thumbnail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videos',
            options={'ordering': ['video', 'thumbnail']},
        ),
        migrations.RenameField(
            model_name='videos',
            old_name='videos',
            new_name='video_url',
        ),
    ]
