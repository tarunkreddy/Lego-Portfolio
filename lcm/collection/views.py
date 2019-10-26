# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum


from .models import LegoSet
from .models import CollectionItem

from bs4 import BeautifulSoup
import requests
import json
from datetime import date, timedelta
from decimal import *
from local_settings import *


# owner = models.CharField(max_length=20)
# 	lego_id = models.ForeignKey(LegoSet)
# 	purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
# 	actual_selling_price = models.DecimalField(max_digits=6, decimal_places=2)
# 	shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)
def index(request):
    collection_list = CollectionItem.objects.all()
    profit = getActualProfit('redwoodclock')
    context = {'collection_list': collection_list, 'profit': profit}
    return render(request, 'collection/view-collection.html', context)


def insert(request):

    try:
        l = LegoSet.objects.get(pk=request.POST['lego_id'])
    except (KeyError, LegoSet.DoesNotExist):
        l = insertNew(request.POST['lego_id'])
    toInsert = CollectionItem(
        owner=request.POST['owner'],
        lego_id=l,
        purchase_price=request.POST['purchase_price'],
        actual_selling_price=request.POST['actual_selling_price'],
        shipping_cost=request.POST['shipping_cost']
    )
    toInsert.save()
    return HttpResponseRedirect(reverse('collection:index'))


def buyingGuide(request, lego_id):
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

    good_buy_estimate = round((avg_price * Decimal(0.90)), 2)

    context = {
        'lego_id': lego_id,
        'name': l.set_name,
        'avg_price': avg_price,
        'good_buy_estimate': good_buy_estimate
    }

    return render(request, 'collection/buying-guide.html', context)


def purchaseHelper(request):
    lego_sets = request.POST['sets']
    lego_sets = lego_sets.strip().split(',')
    sets_info = []
    sale_total = 0
    for lego_set in lego_sets:
        i = getInfo(lego_set)
        sale_total += float(i.estimated_selling_price)
        sets_info.append(i)

    sale_total = round(sale_total, 2)
    context = {'sets_info': sets_info, 'sale_total': sale_total}
    return render(request, 'collection/purchase-helper.html', context)


def retrievePrice(lego_id):
    url = 'http://www.bricklink.com/catalogPG.asp?S=' + lego_id
    headers = {
        'User-Agent': "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    page = requests.get(url, headers=headers)
    source = page.text
    soup = BeautifulSoup(source, 'lxml')
    # name = soup.find('span', id='item-name-title').get_text()
    table = soup.findAll('table')[12]
    rows = table.findAll('td')
    avg_price = rows[7].get_text()
    return Decimal(avg_price[4:])


def retrieveInfo(lego_id):
    url = 'http://www.bricklink.com/catalogPG.asp?S=' + lego_id
    headers = {
        'User-Agent': "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    page = requests.get(url, headers=headers)
    source = page.text
    soup = BeautifulSoup(source, 'lxml')
    # name = soup.find('span', id='item-name-title').get_text()
    name = soup.findAll('table')[3].find('b').get_text()
    table = soup.findAll('table')[12]
    rows = table.findAll('td')
    avg_price = rows[7].get_text()
    return {
        'name': name,
        'estimated_selling_price': float(avg_price[4:])

    }


def getInfo(lego_id):
    try:
        l = LegoSet.objects.get(pk=lego_id)
    except (KeyError, LegoSet.DoesNotExist):
        l = insertNew(lego_id)
    return l


def insertNew(lego_id):
    info = getSet(lego_id)
    price_info = retrieveInfo(lego_id)

    l = LegoSet(
        lego_id=lego_id,
        set_name=info['name'],
        img_url=info['set_img_url'],
        estimated_selling_price=price_info['estimated_selling_price']
    )
    l.save()
    return l


def getSet(lego_id):
    url = 'https://rebrickable.com/api/v3/lego/sets/' + lego_id + '/'
    headers = {'Authorization': 'key ' + REBRICKABLE_API_KEY}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


# Only calculates profit from sold sets; More useful
def getActualProfit(owner):
    c = CollectionItem.objects.filter(owner=owner).exclude(sold=False)
    profit = 0
    for item in c:
        profit += item.profit
    return profit
