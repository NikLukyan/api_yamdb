# Generated by Django 3.2 on 2023-01-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Код авторизации'),
        ),
    ]
