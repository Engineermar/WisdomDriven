# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-23 10:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wdapp', '0012_auto_20181123_1018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='business_email',
            new_name='company_email',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='business_phone_number',
            new_name='company_phone_number',
        ),
        migrations.RemoveField(
            model_name='business',
            name='email',
        ),
        migrations.RemoveField(
            model_name='company',
            name='email',
        ),
    ]
