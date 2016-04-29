# -*- coding: utf-8 -*-
from django.views import generic

from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

from .models import Vid


class DetailView(generic.DetailView):
    model = Vid
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'vid/detail.html'


class VidSearchView(generic.ListView):
    template_name = 'vid/search_list.html'

    def get_queryset(self):
        return SearchQuerySet().filter(content=AutoQuery(self.request.GET.get('query')))
