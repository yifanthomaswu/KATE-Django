# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kateapp', '0002_auto_20161118_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses_Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kateapp.Courses')),
                ('letter_yr', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kateapp.Classes')),
            ],
        ),
        migrations.CreateModel(
            name='Courses_Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kateapp.Courses')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kateapp.Term')),
            ],
        ),
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kateapp.Courses')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('period', models.IntegerField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='exercises',
            unique_together=set([('code', 'number')]),
        ),
    ]