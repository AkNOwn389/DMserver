# Generated by Django 4.2 on 2023-05-10 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_delete_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='NoOfcomment',
            new_name='NoOfComment',
        ),
    ]
