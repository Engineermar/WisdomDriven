# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-21 03:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wdapp', '0007_auto_20170616_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='location',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
