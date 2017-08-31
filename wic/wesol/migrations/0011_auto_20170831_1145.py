# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wesol', '0010_products_actual_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsinvoices',
            name='quantity_remaining',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productsinvoices',
            name='date_expiration',
            field=models.DateField(blank=True, null=True),
        ),
    ]