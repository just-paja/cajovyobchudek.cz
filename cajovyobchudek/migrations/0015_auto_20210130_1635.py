# Generated by Django 3.1.5 on 2021-01-30 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0014_auto_20210130_1629'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopItem',
            new_name='Product',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]