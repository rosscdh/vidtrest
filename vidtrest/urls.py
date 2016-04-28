# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

admin.site.site_header = 'Jonas Hartung - Administration'

urlpatterns = [
    url(r'^vids/', include('vidtrest.apps.vid.urls', namespace='vid')),
    url(r'^admin/', admin.site.urls),
    url(r'^rq/', include('django_rq.urls')),
    url(r'^cat/', include('vidtrest.apps.categories.urls', namespace='categories')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
