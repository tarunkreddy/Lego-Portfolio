# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-02 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0007_collectionitem_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Raffle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raffle_amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='collectionitem',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
    ]
