# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 11:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0015_auto_20170818_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 11, 59, 5, 264000)),
        ),
        migrations.AlterField(
            model_name='clients',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 11, 59, 5, 264000)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 11, 59, 5, 277000)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 11, 59, 5, 277000)),
        ),
    ]
