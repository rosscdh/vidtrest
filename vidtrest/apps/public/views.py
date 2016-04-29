# -*- coding: utf-8 -*-
from django.views import generic


class PublicHomeView(generic.TemplateView):
    template_name = 'public/home.html'

