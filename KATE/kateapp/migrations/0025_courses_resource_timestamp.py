# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kateapp', '0024_auto_20161201_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses_resource',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
