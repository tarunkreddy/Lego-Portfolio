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

from requests_oauthlib import OAuth1


# owner = models.CharField(max_length=20)
# 	lego_id = models.ForeignKey(LegoSet)
# 	purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
# 	actual_selling_price = models.DecimalField(max_digits=6, decimal_places=2)
# 	shipping_cost = models.DecimalField(max_digits=5, decimal_places=2)
def index(request):
    collection_list = CollectionItem.objects.all()
    profitInfo = getActualProfit('redwoodclock')
    unsoldProfit = getPortfolioProfit('redwoodclock')
    raffleProfit = getRaffleProfit('redwoodclock')
    context = {'collection_list': collection_list, 'profitinfo': profitInfo,
               'unsoldprofit': unsoldProfit, 'raffleprofit': raffleProfit}
    return render(request, 'collection/view-collection.html', context)


def insert(request):

    try:
        l = LegoSet.objects.get(pk=request.POST['lego_id'])
    except (KeyError, LegoSet.DoesNotExist):
        l = insertNew(request.POST['lego_id'])
    sold = False
    if (float(request.POST['actual_selling_price']) != 0.0):
        sold = True
    toInsert = CollectionItem(
        owner=request.POST['owner'],
        lego_id=l,
        purchase_price=request.POST['purchase_price'],
        actual_selling_price=request.POST['actual_selling_price'],
        shipping_cost=request.POST['shipping_cost'],
        sold=sold
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
    url = 'https://api.bricklink.com/api/store/v1/items/SET/' + \
        lego_id + '/price?guide_type=sold'
    auth = OAuth1(BRICKLINK_CONSUMER_KEY, BRICKLINK_CONSUMER_SECRET,
                  BRICKLINK_TOKEN_VALUE, BRICKLINK_TOKEN_SECRET)

    response = requests.get(url, auth=auth)

    if response:
        price_guide = response.content.decode('utf-8')
        pg = json.loads(price_guide)
        if (pg['meta']['code'] != 200):
            return
        else:
            return Decimal(pg['data']['avg_price'])
    else:
        return


def getInfo(lego_id):
    try:
        l = LegoSet.objects.get(pk=lego_id)
    except (KeyError, LegoSet.DoesNotExist):
        l = insertNew(lego_id)
    return l


def insertNew(lego_id):
    info = getSet(lego_id)
    price_info = retrievePrice(lego_id)

    l = LegoSet(
        lego_id=lego_id,
        set_name=info['name'],
        img_url=info['set_img_url'],
        estimated_selling_price=price_info
    )
    l.save()
    return l


def getSet(lego_id):
    url = 'https://api.bricklink.com/api/store/v1/items/SET/' + lego_id
    auth = OAuth1(BRICKLINK_CONSUMER_KEY, BRICKLINK_CONSUMER_SECRET,
                  BRICKLINK_TOKEN_VALUE, BRICKLINK_TOKEN_SECRET)
    response = requests.get(url, auth=auth)
    if response:
        set_info = response.content.decode('utf-8')
        info = json.loads(set_info)
        if (info['meta']['code'] != 200):
            return
        else:
            return {'name': info['data']['name'], 'set_img_url': info['data']['thumbnail_url']}
    else:
        return


# Only calculates profit from sold sets;
def getActualProfit(owner):
    c = CollectionItem.objects.filter(owner=owner).exclude(sold=False)
    profit = 0
    normalProfit = 0
    raffleProfit = 0
    for item in c:
        profit += item.profit
        if item.raffle:
            raffleProfit += item.profit
        else:
            normalProfit += item.profit
    return {'profit': profit, 'raffleprofit': raffleProfit, 'normalprofit': normalProfit}


# Returns Value from unsold sets;
def getPortfolioValue(owner):
    c = CollectionItem.objects.filter(owner=owner).exclude(sold=True)
    unsold_value = c.aggregate(Sum('lego_id__estimated_selling_price'))
    return unsold_value


# Get potential Profit from unsold sets;
def getPortfolioProfit(owner):
    c = CollectionItem.objects.filter(owner=owner).exclude(sold=True)
    a = c.aggregate(Sum('lego_id__estimated_selling_price'))[
        'lego_id__estimated_selling_price__sum']
    b = c.aggregate(Sum('purchase_price'))['purchase_price__sum']
    unsold_profit = a - b
    return unsold_profit

# Get Net winnings from raffles;


def getRaffleProfit(owner):
    c = CollectionItem.objects.filter(owner=owner, raffle=True)
    value = c.filter(sold=True).aggregate(Sum('actual_selling_price'))['actual_selling_price__sum'] + \
        c.filter(sold=False).aggregate(Sum('lego_id__estimated_selling_price'))[
        'lego_id__estimated_selling_price__sum']
    cost = c.aggregate(Sum('purchase_price'))[
        'purchase_price__sum'] + c.aggregate(Sum('shipping_cost'))['shipping_cost__sum']
    return value - cost
