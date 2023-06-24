# -*- coding: utf-8 -*-
import django_rq

from django.contrib import admin
from django.urls import include, re_path
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect

from vidtrest.apps.vid.signals import do_upload_to_s3

from .models import Vid, VideoMeta
from .forms import VidForm

queue = django_rq.get_queue('high')


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
            re_path(r'^(?P<pk>.*)/video/$',
                self.admin_site.admin_view(self.view_video),
                name='view_video'),
            re_path(r'^(?P<pk>.*)/re-process/$',
                self.admin_site.admin_view(self.view_reprocess_video),
                name='reprocess_video'),
        ]
        return my_urls + urls

    def get_form(self, *args, **kwargs):
        form = super(NativeAdAdmin, self).get_form(*args, **kwargs)
        form.current_user = args[0].user
        return form

    def view_video(self, request, pk):
        vid = Vid.objects.get(pk=pk)
        context = {
            'is_popup': True,
            'original': vid,
        }
        return render(self.request, 'admin/vid/vid/video_view.html',
                                    context)

    def view_reprocess_video(self, request, pk):
        vid = Vid.objects.get(pk=pk)

        queue.enqueue(do_upload_to_s3,
                      instance=vid)

        messages.info(request, mark_safe('Video has been enqueued for processing: <a href="%s">Track it here</a>' % reverse('rq_home')))

        url = "admin:%s_%s_change" % (vid._meta.app_label,
                                      vid._meta.model_name)

        return redirect(url, pk)


admin.site.register([VideoMeta])
