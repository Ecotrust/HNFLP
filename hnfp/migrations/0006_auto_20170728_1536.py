# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-28 22:36
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hnfp', '0005_auto_20170728_1518'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobopportunity',
            options={'verbose_name_plural': 'Job Opportunities'},
        ),
        migrations.RemoveField(
            model_name='jobopportunity',
            name='apply_url',
        ),
        migrations.RemoveField(
            model_name='jobopportunity',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='jobopportunity',
            name='job_type',
        ),
        migrations.RemoveField(
            model_name='jobopportunity',
            name='location',
        ),
        migrations.RemoveField(
            model_name='jobopportunity',
            name='salary',
        ),
        migrations.AddField(
            model_name='jobopportunity',
            name='html_content',
            field=models.TextField(blank=True, help_text='html if use html == True', null=True),
        ),
        migrations.AddField(
            model_name='jobopportunity',
            name='is_html',
            field=models.BooleanField(default=False, help_text='Use HTML editor'),
        ),
        migrations.AlterField(
            model_name='jobopportunity',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]