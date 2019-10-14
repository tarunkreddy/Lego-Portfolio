# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-13 20:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=20)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('actual_selling_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='LegoSet',
            fields=[
                ('lego_id', models.CharField(default='0', max_length=20, primary_key=True, serialize=False)),
                ('set_name', models.CharField(default='placeholder_name', max_length=100)),
                ('estimated_selling_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price_last_updated', models.DateField(auto_now=True)),
                ('retired', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='collectionitem',
            name='lego_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.LegoSet'),
        ),
    ]
