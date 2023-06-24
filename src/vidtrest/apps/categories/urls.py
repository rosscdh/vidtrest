# -*- coding: utf-8 -*-
from django.urls import include, re_path
from .views import CategoryAndTagsAutocompleteView


urlpatterns = [
    re_path(r'^autocomplete/', CategoryAndTagsAutocompleteView.as_view(), name='autocomplete'),
]
