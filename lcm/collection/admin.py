# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import LegoSet, CollectionItem, Raffle

admin.site.register(LegoSet)
admin.site.register(CollectionItem)
admin.site.register(Raffle)
