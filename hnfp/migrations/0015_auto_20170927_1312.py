# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-27 20:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hnfp', '0014_auto_20170927_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landuseproject',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='date_modified',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='geometry_final',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='geometry_orig',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='manipulators',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='sharing_groups',
        ),
        migrations.RemoveField(
            model_name='landuseproject',
            name='user',
        ),
    ]