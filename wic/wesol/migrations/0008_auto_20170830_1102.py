# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wesol', '0007_dailyreport_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='number',
            field=models.CharField(max_length=10),
        ),
    ]