# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-09 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0030_remove_timedate_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='timedate',
            name='time',
            field=models.DateTimeField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='images',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
