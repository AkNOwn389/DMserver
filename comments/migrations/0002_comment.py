# Generated by Django 4.2 on 2023-05-10 01:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_delete_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.UUIDField()),
                ('avatar', models.ImageField(blank=True, upload_to='')),
                ('comment_type', models.IntegerField(default=1)),
                ('comments', models.TextField(max_length=1500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('NoOflike', models.IntegerField(default=0)),
                ('isDeleted', models.BooleanField(default=False)),
                ('image', models.ManyToManyField(blank=True, to='posts.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ManyToManyField(blank=True, to='posts.videos')),
            ],
        ),
    ]