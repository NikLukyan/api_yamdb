# Generated by Django 3.2 on 2023-01-20 15:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together={('title', 'author')},
        ),
    ]
