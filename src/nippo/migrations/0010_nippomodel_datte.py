# Generated by Django 5.0.1 on 2024-01-24 07:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nippo', '0009_alter_nippomodel_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='nippomodel',
            name='datte',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
