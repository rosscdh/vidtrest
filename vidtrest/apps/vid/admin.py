# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import url
from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import Vid, VideoMeta
from .forms import VidForm


@admin.register(Vid)
class NativeAdAdmin(admin.ModelAdmin):
    form = VidForm
    list_per_page = 100

    list_display = ('name',)
    list_filter = ('categories',)
    search_fields = ['name', 'tags__name']

    def get_urls(self):
        urls = super(NativeAdAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>.*)/video/$',
                self.admin_site.admin_view(self.view_video),
                name='view_video'),
        ]
        return my_urls + urls

    def view_video(self, request, pk):
        vid = Vid.objects.get(pk=pk)
        context = {
            'is_popup': True,
            'original': vid,
        }
        return render_to_response('admin/vid/vid/video_view.html',
                                  context,
                                  context_instance=RequestContext(request))


admin.site.register([VideoMeta])