# Generated by Django 4.2 on 2023-04-09 14:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_alter_videos_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
