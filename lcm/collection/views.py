# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import LegoSet
from .models import CollectionItem

from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta

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

def checkPrice(request, lego_id):
	try:
		l = LegoSet.objects.get(pk=lego_id)
	except (KeyError, LegoSet.DoesNotExist):
		return HttpResponseRedirect(reverse('collection:index'))
	if l.price_last_updated <= date.today()-timedelta(days=7):
		avg_price = retrievePrice(lego_id)
		l.estimated_selling_price = avg_price
		l.save()
	else:
		avg_price = l.estimated_selling_price

	return HttpResponse("The price for set " + lego_id + " is " + str(avg_price))


def retrievePrice(lego_id):
	url = 'http://www.bricklink.com/catalogPG.asp?S=' + lego_id
	headers = {'User-Agent': "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
	page = requests.get(url, headers=headers)
	source = page.text
	soup = BeautifulSoup(source, 'lxml')
	# name = soup.find('span', id='item-name-title').get_text()
	table = soup.findAll('table')[12]
	rows = table.findAll('td')
	avg_price = rows[7].get_text()
	return float(avg_price[4:])


