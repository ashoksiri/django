# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 12:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0016_auto_20170914_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 12, 0, 17, 163000)),
        ),
        migrations.AlterField(
            model_name='clients',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 12, 0, 17, 163000)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 12, 0, 17, 174000)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 12, 0, 17, 174000)),
        ),
    ]