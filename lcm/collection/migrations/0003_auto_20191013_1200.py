# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-13 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20191013_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='legoset',
            name='price_last_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='legoset',
            name='retired',
            field=models.BooleanField(default=True),
        ),
    ]