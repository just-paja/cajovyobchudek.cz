# Generated by Django 3.1.5 on 2021-01-30 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0018_auto_20210130_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='product_tags', to='cajovyobchudek.tag', verbose_name='Tag'),
        ),
    ]
