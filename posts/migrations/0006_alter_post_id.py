# Generated by Django 4.0 on 2023-03-27 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
