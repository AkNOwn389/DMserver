# Generated by Django 4.0 on 2023-03-28 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]
