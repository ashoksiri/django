# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 14:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanage', '0006_auto_20170814_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 20, 13, 21, 92420)),
        ),
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='clients',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 20, 13, 21, 92487)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 20, 13, 21, 99545)),
        ),
        migrations.AlterField(
            model_name='countries',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 14, 20, 13, 21, 99607)),
        ),
    ]
