# Generated by Django 3.1.5 on 2021-01-30 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0019_auto_20210130_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttag',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Product Weight'),
        ),
    ]