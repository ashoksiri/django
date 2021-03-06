# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 09:36
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('age', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.IntegerField(default=False)),
                ('user_type', models.CharField(default='user', max_length=10)),
                ('is_preferences_active', models.IntegerField(default=False)),
                ('row_status', models.BooleanField(default=True)),
                ('requested_by', models.CharField(blank=True, max_length=10, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('created_time', models.DateTimeField(blank=True, null=True, verbose_name='date created')),
                ('modified_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Channel_page_sources',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('source_type', models.CharField(max_length=50)),
                ('channel_page', models.CharField(max_length=100)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('row_status', models.CharField(blank=True, max_length=10, null=True)),
                ('requested_by', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('city_name', models.CharField(max_length=20)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('organisation_name', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('contact_number', models.CharField(max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(max_length=20)),
                ('row_status', models.CharField(default=1, max_length=2)),
                ('requested_by', models.CharField(max_length=10)),
                ('created_time', models.DateTimeField(default=datetime.datetime(2017, 8, 11, 15, 6, 51, 764528))),
                ('modified_time', models.DateTimeField(default=datetime.datetime(2017, 8, 11, 15, 6, 51, 764577))),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=20, unique=True)),
                ('created_time', models.DateTimeField(default=datetime.datetime(2017, 8, 11, 15, 6, 51, 761618))),
                ('modified_time', models.DateTimeField(default=datetime.datetime(2017, 8, 11, 15, 6, 51, 761715))),
            ],
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=50)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanage.Clients')),
            ],
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('requested_by', models.CharField(blank=True, max_length=10, null=True)),
                ('row_status', models.CharField(max_length=10, null=True)),
                ('keywords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanage.Keywords')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state_name', models.CharField(max_length=20, unique=True)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('countries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanage.Countries')),
            ],
        ),
        migrations.AddField(
            model_name='cities',
            name='states',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanage.States'),
        ),
        migrations.AddField(
            model_name='channel_page_sources',
            name='clients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanage.Clients'),
        ),
    ]
