from django.conf.urls import url, include

from . import views

app_name = 'vids'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]