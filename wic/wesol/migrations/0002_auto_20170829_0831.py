# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wesol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='name',
            field=models.IntegerField(choices=[(1, 'Kasa Główna'), (2, 'Kasa Fiskalna'), (3, 'Konto Bankowe IDEA'), (4, 'Konto Bankowe INTELIGO'), (5, 'Konto Bankowe NEST')]),
        ),
    ]
