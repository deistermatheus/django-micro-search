# Generated by Django 5.0.6 on 2024-06-22 22:48

import pgvector.django
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('blob_metadata', models.JSONField(default=dict)),
                ('image_embedding', pgvector.django.VectorField(dimensions=512, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]