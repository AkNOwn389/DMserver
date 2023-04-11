# Generated by Django 4.2 on 2023-04-10 00:33

import cloudinary_storage.storage
from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0026_alter_videos_videos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(blank=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='posts_images/thumbnails/', verbose_name='thumbnail'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='videos',
            field=models.FileField(storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage(), upload_to=posts.models.post_videos_rdm_name),
        ),
    ]