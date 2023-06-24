# -*- coding: utf-8 -*-
from django.urls import include, re_path

from . import views

urlpatterns = [
    re_path(r'^search/$', views.VidSearchView.as_view(), name='search'),
    re_path(r'^(?P<uuid>[0-9a-z-]+)/$', views.DetailView.as_view(), name='detail'),
]