# Generated by Django 4.2 on 2023-04-24 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_comment_image_comment_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='type',
            new_name='comment_type',
        ),
    ]
