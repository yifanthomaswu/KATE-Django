# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-05 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kateapp', '0029_exercises_marked'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercises',
            name='released',
            field=models.BooleanField(default=False),
        ),
    ]
