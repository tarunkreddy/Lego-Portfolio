# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import LegoSet
from .models import CollectionItem

# owner = models.CharField(max_length=20)
# 	lego_id = models.ForeignKey(LegoSet)
# 	purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
# 	actual_selling_price = models.DecimalField(max_digits=6, decimal_places=2)
# 	shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)
def index(request):
	collection_list = CollectionItem.objects.all()
	context = {'collection_list': collection_list}
	return render(request, 'collection/view-collection.html', context)


def insert(request):

	try:
		l = LegoSet.objects.get(pk=request.POST['lego_id'])
	except (KeyError, LegoSet.DoesNotExist):
		return HttpResponseRedirect(reverse('collection:index'))
	toInsert = CollectionItem(
		owner=request.POST['owner'],
		lego_id=l,
		purchase_price=request.POST['purchase_price'],
		actual_selling_price=request.POST['actual_selling_price'],
		shipping_cost=request.POST['shipping_cost']
		)
	toInsert.save()
	return HttpResponseRedirect(reverse('collection:index'))
