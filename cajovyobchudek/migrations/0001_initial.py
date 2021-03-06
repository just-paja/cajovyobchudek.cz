# Generated by Django 3.1.4 on 2020-12-22 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.PositiveIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday'), (8, 'Weekend'), (9, 'Workweek'), (10, 'Public holiday')], verbose_name='Weekday')),
                ('from_hour', models.TimeField(verbose_name='Opening')),
                ('to_hour', models.TimeField(verbose_name='Closing')),
            ],
            options={
                'verbose_name': 'Business Hours',
                'verbose_name_plural': 'Business Hours',
                'ordering': ['weekday', 'from_hour'],
            },
        ),
        migrations.CreateModel(
            name='ClosingRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='Start')),
                ('end', models.DateTimeField(verbose_name='End')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='Reason')),
            ],
            options={
                'verbose_name': 'Closing Rule',
                'verbose_name_plural': 'Closing Rules',
                'ordering': ['start'],
            },
        ),
    ]
