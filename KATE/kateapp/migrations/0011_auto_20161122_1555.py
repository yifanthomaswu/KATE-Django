# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kateapp', '0010_auto_20161122_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='assessment',
            field=models.CharField(choices=[('NO', 'No Assessment'), ('INDIVIDUAL', 'Individual'), ('GROUP', 'Group')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='exercises',
            name='submission',
            field=models.CharField(choices=[('NO', 'No submission'), ('HARDCOPY', 'Hardcopy'), ('ELECTRONIC', 'Electronic')], max_length=15, null=True),
        ),
    ]