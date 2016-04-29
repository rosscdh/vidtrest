# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views import generic

from .views import PublicHomeView, SearchAutocompleteView


urlpatterns = [
    url(r'^search/autocomplete/',
        SearchAutocompleteView.as_view(),
        name='search_autocomplete'),

    url(r'^$', PublicHomeView.as_view(),
        name='home'),

    url(r'^about/$', generic.TemplateView.as_view(template_name='public/about.html'),
        name='about')
]
