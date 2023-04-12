# Generated by Django 4.2 on 2023-04-13 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleonetooneroom',
            name='id',
            field=models.UUIDField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='PrivateRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connected_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatMate', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_connector', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
