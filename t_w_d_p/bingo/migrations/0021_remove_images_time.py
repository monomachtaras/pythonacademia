# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-09 17:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0020_auto_20170209_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='time',
        ),
    ]