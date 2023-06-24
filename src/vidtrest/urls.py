# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static

admin.site.site_header = 'Vidtrest - Administration'

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^rq/', include('django_rq.urls')),
    re_path(r'^cat/', include(('vidtrest.apps.categories.urls', 'categories'), namespace='categories')),
    re_path(r'^vids/', include(('vidtrest.apps.vid.urls', 'vid'), namespace='vid')),
    re_path(r'^', include(('vidtrest.apps.public.urls', 'public'), namespace='public')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
