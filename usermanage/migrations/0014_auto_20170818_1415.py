# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 14:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0013_auto_20170817_1640'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.AddField(
            model_name='channel_page_sources',
            name='status',
            field=models.IntegerField(default=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 18, 14, 15, 48, 747764)),
        ),
        migrations.AlterField(
            model_name='clients',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 18, 14, 15, 48, 747813)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 18, 14, 15, 48, 754400)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 18, 14, 15, 48, 754447)),
        ),
    ]
