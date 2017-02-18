# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-03 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='age',
            name='number',
        ),
        migrations.AddField(
            model_name='age',
            name='number',
            field=models.ManyToManyField(to='bingo.Number'),
        ),
        migrations.RemoveField(
            model_name='city',
            name='number',
        ),
        migrations.AddField(
            model_name='city',
            name='number',
            field=models.ManyToManyField(to='bingo.Number'),
        ),
    ]