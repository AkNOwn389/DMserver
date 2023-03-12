# Generated by Django 4.0 on 2023-03-12 15:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegisterCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid3, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('code', models.IntegerField(max_length=8)),
                ('expiration', models.DateTimeField(db_index=True)),
            ],
        ),
    ]
