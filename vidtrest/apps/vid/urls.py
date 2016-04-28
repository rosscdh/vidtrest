# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<uuid>[^/]+)/$', views.DetailView.as_view(), name='detail'),
]