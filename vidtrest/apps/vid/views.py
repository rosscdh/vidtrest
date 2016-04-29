# -*- coding: utf-8 -*-
from django.views import generic
from haystack.generic_views import SearchView
from .models import Vid


class DetailView(generic.DetailView):
    model = Vid
    template_name = 'vid/detail.html'


class VidSearchView(SearchView):
    template_name = 'vid/search_list.html'