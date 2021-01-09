# Generated by Django 3.1.4 on 2021-01-09 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0005_tagconnection_weight'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='tagconnection',
            options={'verbose_name': 'Tag Connection', 'verbose_name_plural': 'Tag Connections'},
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='', max_length=63),
            preserve_default=False,
        ),
    ]
