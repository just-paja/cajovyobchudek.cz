# Generated by Django 3.1.5 on 2021-02-07 13:43
import os

from django.core import serializers
from django.db import migrations

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
FIXTURE_FILENAME = 'products-pre-2020.json'


def load_fixture(apps, schema_editor):

    fixture_file = os.path.join(fixture_dir, FIXTURE_FILENAME)
    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
    for obj in objects:
        obj.save()
    fixture.close()


class Migration(migrations.Migration):

    dependencies = [
        ('cajovyobchudek', '0028_initial_tags'),
    ]

    operations = [
            migrations.RunPython(load_fixture)
    ]
