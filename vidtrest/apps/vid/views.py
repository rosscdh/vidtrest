from django.http import HttpResponseRedirect
from django.views import generic

from .models import Vid


class DetailView(generic.DetailView):
    model = Vid
    template_name = 'vid/detail.html'
