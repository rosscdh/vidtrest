# -*- coding: utf-8 -*-
from django.views import generic

from .models import Vid


class DetailView(generic.DetailView):
    model = Vid
    # slug_field = 'uuid'
    # slug_url_kwarg = 'uuid'
    template_name = 'vid/detail.html'
