# Generated by Django 3.1.4 on 2020-12-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0002_auto_20201227_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitealert',
            name='severity',
            field=models.PositiveIntegerField(choices=[(1, 'Informative'), (2, 'Warning'), (3, 'Danger')], default=1),
        ),
    ]