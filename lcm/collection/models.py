# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class LegoSet(models.Model):
	lego_id = models.IntegerField(default=0, primary_key=True)
	set_name = models.CharField(default='placeholder_name', max_length=100)
	estimated_selling_price = models.DecimalField(max_digits=6, decimal_places=2)
	price_last_updated = models.DateField(auto_now=True)
	retired = models.BooleanField(default=True)
	

	def __str__(self):
		return str(self.lego_id) + '-' + self.set_name

class CollectionItem(models.Model):
	owner = models.CharField(max_length=20, primary_key=True)
	lego_id = models.ForeignKey(LegoSet)
	purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
	actual_selling_price = models.DecimalField(max_digits=6, decimal_places=2)
	shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return self.owner + "'s " + str(self.lego_id) + ': Paid ' + str(self.purchase_price+self.shipping_cost) + ', Sold for ' + str(self.actual_selling_price) 
