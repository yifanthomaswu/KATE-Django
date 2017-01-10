# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-10 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kateapp', '0032_auto_20170106_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses_resource',
            name='course_resource_type',
            field=models.CharField(choices=[('NOTE', 'Note'), ('PROBLEM', 'Problem'), ('URL', 'Url'), ('PANOPTO', 'Panopto'), ('PIAZZA', 'Piazza'), ('HOMEPAGE', 'Homepage')], default='NOTE', max_length=15),
        ),
    ]