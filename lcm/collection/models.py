# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime


@python_2_unicode_compatible
class LegoSet(models.Model):
    lego_id = models.CharField(default='0', max_length=20, primary_key=True)
    set_name = models.CharField(default='placeholder_name', max_length=100)
    estimated_selling_price = models.DecimalField(
        max_digits=6, decimal_places=2)
    price_last_updated = models.DateField(auto_now=True)
    img_url = models.URLField(default="")
    retired = models.BooleanField(default=True)

    def __str__(self):
        return self.lego_id + '-' + self.set_name


@python_2_unicode_compatible
class CollectionItem(models.Model):
    owner = models.CharField(max_length=20)
    lego_id = models.ForeignKey(LegoSet)
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
    actual_selling_price = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)
    sold = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    raffle = models.BooleanField(default=False)
    date_purchased = models.DateField(default=datetime.now)
    notes = models.TextField(default="", blank=True)

    @property
    def profit(self):
        return (self.actual_selling_price - self.purchase_price - self.shipping_cost)

    def __str__(self):
        return self.owner + \
            "'s " + \
            str(self.lego_id) + \
            ': Paid ' + \
            str(self.purchase_price+self.shipping_cost) + \
            ', Sold for ' + str(self.actual_selling_price) + \
            ', PROFIT: ' + str(self.profit)


@python_2_unicode_compatible
class Raffle(models.Model):
    raffle_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.raffle_amount)
