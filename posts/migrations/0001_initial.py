# Generated by Django 4.1.7 on 2023-04-01 01:29

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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=500, upload_to=posts.models.post_rdm_name, verbose_name='Image')),
            ],
            options={
                'ordering': ['image'],
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videos', models.ImageField(upload_to=posts.models.post_videos_rdm_name)),
            ],
            options={
                'ordering': ['videos'],
            },
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
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('images_url', models.ManyToManyField(blank=True, to='posts.image')),
                ('videos_url', models.ManyToManyField(blank=True, to='posts.videos')),
            ],
            options={
                'ordering': ('-created_at',),
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
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.UUIDField()),
                ('avatar', models.ImageField(blank=True, upload_to='')),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('type', models.IntegerField(default=1)),
                ('comments', models.TextField(max_length=1500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
