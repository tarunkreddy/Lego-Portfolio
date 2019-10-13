# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import LegoSet
from .models import CollectionItem


def index(request):
	collection_list = CollectionItem.objects.all()
	context = {'collection_list': collection_list}
	return render(request, 'collection/view-collection.html', context)


def addSet(request):
	return
