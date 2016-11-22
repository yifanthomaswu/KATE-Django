# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kateapp', '0013_auto_20161122_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='submission',
            field=models.CharField(choices=[('NO', 'No submission'), ('HARDCOPY', 'Hardcopy'), ('ELECTRONIC', 'Electronic')], default='NO', max_length=15),
        ),
    ]