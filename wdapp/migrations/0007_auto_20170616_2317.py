# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-16 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wdapp', '0006_auto_20170615_0314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetails',
            old_name='quanity',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='create_at',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Cooking'), (2, 'Ready'), (3, 'On the way'), (4, 'Delivered')]),
        ),
    ]
