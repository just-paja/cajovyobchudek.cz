# Generated by Django 3.1.5 on 2021-01-10 11:37

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0009_auto_20210109_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=markdownfield.models.MarkdownField(blank=True, null=True, verbose_name='Description'),
        ),
    ]