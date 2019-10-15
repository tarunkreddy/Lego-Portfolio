from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^insert/$', views.insert, name='insert'),
	url(r'^check/(?P<lego_id>[0-9a-zA-Z]+-?[0-9])/$', views.checkPrice, name='check')
]