# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import PublicHomeView, SearchAutocompleteView


urlpatterns = [
    url(r'^search/autocomplete/',
        SearchAutocompleteView.as_view(),
        name='search_autocomplete'),

    url(r'^$', PublicHomeView.as_view(),
        name='home')
]
