# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-04 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hnfp', '0014_auto_20171102_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='landuseproject',
            name='share_with_land_managers',
            field=models.BooleanField(default=False),
        ),
    ]