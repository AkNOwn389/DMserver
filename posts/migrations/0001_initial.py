# Generated by Django 4.2 on 2023-04-24 02:08

import cloudinary.models
import cloudinary_storage.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=posts.models.get_unique_id, primary_key=True, serialize=False)),
                ('public_id', models.TextField(default='null', max_length=300)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('NoOflike', models.IntegerField(default=0)),
                ('NoOfcomment', models.IntegerField(default=0)),
                ('url', models.URLField(blank=True)),
                ('url_w1000', models.URLField(blank=True)),
                ('url_w250', models.URLField(blank=True)),
                ('secure_url', models.URLField(blank=True)),
                ('width', models.TextField(blank=True)),
                ('height', models.TextField(blank=True)),
                ('thumbnail', models.TextField(blank=True)),
                ('asset_id', models.TextField(blank=True)),
                ('version', models.TextField(blank=True)),
                ('version_id', models.TextField(blank=True)),
                ('signature', models.TextField(blank=True)),
                ('Format', models.TextField(blank=True)),
                ('resource_type', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Bytes', models.TextField(blank=True)),
                ('Type', models.TextField(blank=True)),
                ('etag', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['image', 'NoOflike', 'NoOfcomment', 'thumbnail'],
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('public_id', models.TextField(default='null', max_length=300)),
                ('videos', cloudinary.models.CloudinaryField(max_length=255, verbose_name='video')),
                ('original', models.URLField(blank=True)),
                ('playback_url', models.URLField(blank=True)),
                ('url_w1000', models.URLField(blank=True)),
                ('url_w500', models.URLField(blank=True)),
                ('url_w250', models.URLField(blank=True)),
                ('secure_url', models.URLField(blank=True)),
                ('audio_bit_rate', models.TextField(blank=True)),
                ('audio_codec', models.TextField(blank=True)),
                ('frequency', models.TextField(blank=True)),
                ('channels', models.TextField(blank=True)),
                ('channel_layout', models.TextField(blank=True)),
                ('width', models.TextField(blank=True)),
                ('height', models.TextField(blank=True)),
                ('thumbnail', models.URLField(blank=True)),
                ('asset_id', models.TextField(blank=True)),
                ('version', models.TextField(blank=True)),
                ('version_id', models.TextField(blank=True)),
                ('signature', models.TextField(blank=True)),
                ('Format', models.TextField(blank=True)),
                ('resource_type', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Bytes', models.TextField(blank=True)),
                ('Type', models.TextField(blank=True)),
                ('etag', models.TextField(blank=True)),
                ('is_audio', models.BooleanField(default=False)),
                ('framerate', models.IntegerField(blank=True)),
                ('bit_rate', models.TextField(blank=True)),
                ('duration', models.IntegerField(blank=True)),
                ('rotation', models.IntegerField(default=0)),
                ('original_filename', models.TextField(blank=True)),
                ('nb_frames', models.IntegerField(blank=True)),
                ('api_key', models.TextField(blank=True)),
                ('pix_format', models.TextField(blank=True)),
                ('video_codec', models.TextField(blank=True)),
                ('level', models.TextField(blank=True)),
                ('profile', models.TextField(blank=True)),
                ('video_bitrate', models.TextField(blank=True)),
                ('time_base', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('source', models.TextField(default='direct message', max_length=200)),
                ('creator_full_name', models.TextField(max_length=200)),
                ('title', models.TextField(blank=True)),
                ('perma_link', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('status', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('NoOflike', models.IntegerField(default=0)),
                ('NoOfcomment', models.IntegerField(default=0)),
                ('media_type', models.IntegerField(default=1)),
                ('privacy', models.CharField(choices=[('P', 'Public'), ('F', 'Friends'), ('O', 'Only-Me')], default='F', max_length=1)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('images_url', models.ManyToManyField(blank=True, related_name='images', to='posts.image')),
                ('videos_url', models.ManyToManyField(blank=True, related_name='video', to='posts.videos')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentId', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.UUIDField()),
                ('avatar', models.ImageField(blank=True, upload_to='')),
                ('image', models.ImageField(blank=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='')),
                ('type', models.IntegerField(default=1)),
                ('comments', models.TextField(max_length=1500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('NoOflike', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
