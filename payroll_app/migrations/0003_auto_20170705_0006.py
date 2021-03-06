# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-04 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0002_auto_20170702_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary_per_day',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
