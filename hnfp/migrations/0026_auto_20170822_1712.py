# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-23 00:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hnfp', '0025_auto_20170822_1446'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ObservationCategory',
        ),
        migrations.DeleteModel(
            name='ObservationLocation',
        ),
    ]