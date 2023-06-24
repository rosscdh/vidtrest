# -*- coding: utf-8 -*-
from django.urls import include, re_path
from django.views import generic

from .views import PublicHomeView, SearchAutocompleteView


urlpatterns = [
    re_path(r'^search/autocomplete/',
        SearchAutocompleteView.as_view(),
        name='search_autocomplete'),

    re_path(r'^$', PublicHomeView.as_view(),
        name='home'),

    re_path(r'^about/$', generic.TemplateView.as_view(template_name='public/about.html'),
        name='about')
]
