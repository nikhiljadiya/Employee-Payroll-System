# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0006_auto_20170711_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='punch_in_time',
            field=models.TimeField(null=True),
        ),
    ]