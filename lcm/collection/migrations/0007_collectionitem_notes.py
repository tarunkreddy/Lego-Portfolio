# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-01 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_collectionitem_raffle'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionitem',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]