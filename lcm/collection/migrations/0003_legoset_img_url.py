# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-16 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_collectionitem_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='legoset',
            name='img_url',
            field=models.URLField(default=''),
        ),
    ]