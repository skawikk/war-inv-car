# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wesol', '0004_dailyreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='number',
            field=models.IntegerField(),
        ),
    ]
