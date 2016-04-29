# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import PublicHomeView


urlpatterns = [
    url(r'^$', PublicHomeView.as_view(), name='home'),
]
