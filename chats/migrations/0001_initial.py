# Generated by Django 4.1.7 on 2023-03-11 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subscribers', models.ManyToManyField(blank=True, to='profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='RoomMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=1500)),
                ('msg_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.room')),
            ],
        ),
        migrations.CreateModel(
            name='OnlineUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('chat_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('users', models.ManyToManyField(related_name='room_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messageid', models.UUIDField()),
                ('body', models.TextField(max_length=1500)),
                ('created_at', models.DateField(default='2023-03-11')),
                ('created_time', models.TimeField(default='13:38:11.85995')),
                ('seen', models.BooleanField(default=False)),
                ('msg_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_receiver', to=settings.AUTH_USER_MODEL)),
                ('msg_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]