# Generated by Django 3.1.5 on 2021-01-30 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0023_tag_main_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=None, max_length=127, unique=True),
            preserve_default=False,
        ),
    ]
