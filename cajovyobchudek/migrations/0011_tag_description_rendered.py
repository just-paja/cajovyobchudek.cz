# Generated by Django 3.1.5 on 2021-01-10 11:39

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0010_auto_20210110_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='description_rendered',
            field=markdownfield.models.RenderedMarkdownField(null=True),
        ),
    ]
