# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-15 00:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hnfp', '0019_auto_20180413_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='category',
            field=models.CharField(choices=[('Bear', 'bear'), ('Deer', 'deer'), ('Medicinal Herbs', 'medicinal_herbs'), ('Shrimp', 'shrimp'), ('Berries', 'berries'), ('Firewood', 'firewood'), ('Mushrooms', 'mushrooms'), ('Crab', 'crab'), ('Shellfish', 'shellfish'), ('Salmon', 'salmon'), ('Other Fish', 'other_fish'), ('Basket Making', 'basket_making'), ('Custom', 'custom')], default='custom', max_length=400),
        ),
    ]
