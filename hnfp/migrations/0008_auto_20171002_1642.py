# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-02 23:42
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hnfp', '0007_auto_20171002_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresults',
            name='forest_use',
            field=models.CharField(blank=True, choices=[('Hunt', 'hunt_deer'), ('Gather Herbs', 'gather_herbs'), ('Fish', 'fish'), ('Collect Berries', 'collect_berries'), ('Gather Mushrooms', 'gather_mushrooms'), ('Collect Firewood', 'collect_firewood'), ('Other/None', 'other')], max_length=400, null=True),
        ),
    ]