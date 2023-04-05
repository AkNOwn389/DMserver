# Generated by Django 4.0 on 2023-04-03 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_privacy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='post',
            name='images_url',
            field=models.ManyToManyField(blank=True, related_name='images', to='posts.Image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='videos_url',
            field=models.ManyToManyField(blank=True, related_name='video', to='posts.Videos'),
        ),
    ]
