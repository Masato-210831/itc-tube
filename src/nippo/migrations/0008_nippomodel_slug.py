# Generated by Django 5.0.1 on 2024-01-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nippo', '0007_nippomodel_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='nippomodel',
            name='slug',
            field=models.SlugField(blank=True, max_length=20, null=True),
        ),
    ]
