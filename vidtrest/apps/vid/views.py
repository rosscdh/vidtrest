# -*- coding: utf-8 -*-
from django.views import generic

from .models import Vid


class DetailView(generic.DetailView):
    model = Vid
    template_name = 'vid/detail.html'
