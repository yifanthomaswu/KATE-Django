# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kateapp', '0007_auto_20161122_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='assessment',
            field=models.CharField(blank=True, choices=[('', 'No Assessment'), ('INDIVIDUAL', 'Individual'), ('GROUP', 'Group')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='exercises',
            name='submission',
            field=models.CharField(blank=True, choices=[('', 'No submission'), ('HARDCOPY', 'Hardcopy'), ('ELECTRONIC', 'Electronic')], max_length=15, null=True),
        ),
    ]
