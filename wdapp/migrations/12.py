# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-23 10:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wdapp', '0011_auto_20181123_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='company',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='slug',
        ),
    ]
