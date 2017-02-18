# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 18:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('html_href', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField(unique=True)),
                ('ages', models.ManyToManyField(to='bingo.Age')),
                ('cities', models.ManyToManyField(to='bingo.City')),
                ('images', models.ManyToManyField(to='bingo.Images')),
            ],
        ),
        migrations.CreateModel(
            name='TimeDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bingo.Number')),
            ],
        ),
    ]