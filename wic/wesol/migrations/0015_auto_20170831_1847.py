# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wesol', '0014_contractors_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractors',
            name='nip',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
