# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 16:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wesol', '0013_auto_20170831_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractors',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
