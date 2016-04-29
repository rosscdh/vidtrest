# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/$', views.VidSearchView.as_view(), name='search'),
    url(r'^(?P<uuid>[0-9a-z-]+)/$', views.DetailView.as_view(), name='detail'),
]