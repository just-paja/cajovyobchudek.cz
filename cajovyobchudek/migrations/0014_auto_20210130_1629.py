# Generated by Django 3.1.5 on 2021-01-30 15:29

import cajovyobchudek.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0013_auto_20210130_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', cajovyobchudek.models.fields.DescriptionField(blank=True, null=True, rendered_field='text_rendered', verbose_name='Description')),
                ('text_rendered', cajovyobchudek.models.fields.RenderedDescriptionField(null=True)),
            ],
            options={
                'verbose_name': 'Product Description',
                'verbose_name_plural': 'Product Descriptions',
            },
        ),
        migrations.CreateModel(
            name='ProductUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', cajovyobchudek.models.fields.DescriptionField(blank=True, null=True, rendered_field='text_rendered', verbose_name='Description')),
                ('text_rendered', cajovyobchudek.models.fields.RenderedDescriptionField(null=True)),
            ],
            options={
                'verbose_name': 'Product Usage',
                'verbose_name_plural': 'Product Usages',
            },
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='shopitem',
            options={'verbose_name': 'Shop Item', 'verbose_name_plural': 'Shop Items'},
        ),
        migrations.RemoveField(
            model_name='shopitem',
            name='description_rendered',
        ),
        migrations.RemoveField(
            model_name='shopitem',
            name='usage_rendered',
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=cajovyobchudek.models.fields.NameField(max_length=63, unique=True, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='distributor',
            field=cajovyobchudek.models.fields.FaculativeForeignKey(blank=True, help_text='Product maker, creator, author', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distributed_items', to='cajovyobchudek.company', verbose_name='Distributor'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='local_name',
            field=cajovyobchudek.models.fields.NameField(help_text='Define the localized name, for example "Nefritová Bohyně Milosrdenství"', max_length=63, verbose_name='Localized Name'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='name',
            field=cajovyobchudek.models.fields.NameField(help_text='Define the original product name, for example "Yu Guan Yin"', max_length=63, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='producer',
            field=cajovyobchudek.models.fields.FaculativeForeignKey(blank=True, help_text='Product maker, creator, author', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produced_items', to='cajovyobchudek.company', verbose_name='Producer'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='description',
            field=cajovyobchudek.models.fields.FaculativeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='cajovyobchudek.productdescription', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='shopitem',
            name='usage',
            field=cajovyobchudek.models.fields.FaculativeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='cajovyobchudek.productusage', verbose_name='Usage'),
        ),
    ]
