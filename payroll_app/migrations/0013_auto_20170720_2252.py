# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-20 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0012_auto_20170718_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]