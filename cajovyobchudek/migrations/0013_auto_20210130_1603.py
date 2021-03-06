# Generated by Django 3.1.5 on 2021-01-30 15:03

import cajovyobchudek.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0012_auto_20210110_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', cajovyobchudek.models.fields.NameField(max_length=63, unique=True, verbose_name='Name')),
            ],
        ),
        migrations.AlterModelOptions(
            name='sitealert',
            options={'verbose_name': 'Site Alert', 'verbose_name_plural': 'Site Alerts'},
        ),
        migrations.AlterField(
            model_name='sitealert',
            name='name',
            field=cajovyobchudek.models.fields.NameField(max_length=31, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=cajovyobchudek.models.fields.DescriptionField(blank=True, null=True, rendered_field='description_rendered', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='description_rendered',
            field=cajovyobchudek.models.fields.RenderedDescriptionField(null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=cajovyobchudek.models.fields.NameField(max_length=63, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='public',
            field=cajovyobchudek.models.fields.VisibilityField(default=True, verbose_name='Public'),
        ),
        migrations.CreateModel(
            name='ShopItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', cajovyobchudek.models.fields.NameField(help_text='Define the original product name, for example "Yu Guan Yin"', max_length=63, verbose_name='Name')),
                ('local_name', cajovyobchudek.models.fields.NameField(help_text='Define the localized name, for example "Nefritová Bohyně Milosrdenství"', max_length=63, verbose_name='Name')),
                ('public', cajovyobchudek.models.fields.VisibilityField(default=True, verbose_name='Public')),
                ('product_code', models.PositiveIntegerField(blank=True, help_text='Product number, barcode number', null=True, verbose_name='Product Code')),
                ('description', cajovyobchudek.models.fields.DescriptionField(blank=True, null=True, rendered_field='description_rendered', verbose_name='Description')),
                ('description_rendered', cajovyobchudek.models.fields.RenderedDescriptionField(null=True)),
                ('usage', cajovyobchudek.models.fields.DescriptionField(blank=True, null=True, rendered_field='usage_rendered', verbose_name='Description')),
                ('usage_rendered', cajovyobchudek.models.fields.RenderedDescriptionField(null=True)),
                ('distributor', models.ForeignKey(blank=True, help_text='Product maker, creator, author', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distributed_items', to='cajovyobchudek.company', verbose_name='Distributor')),
                ('producer', models.ForeignKey(blank=True, help_text='Product maker, creator, author', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produced_items', to='cajovyobchudek.company', verbose_name='Producer')),
            ],
        ),
    ]
