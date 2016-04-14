# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import CategoryAndTagsAutocompleteView


urlpatterns = [
    url(r'^autocomplete/', CategoryAndTagsAutocompleteView.as_view(), name='autocomplete'),
]
