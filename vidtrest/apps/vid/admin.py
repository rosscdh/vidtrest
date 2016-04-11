# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponse
from django.utils.safestring import mark_safe
#from advanced_filters.admin import AdminAdvancedFiltersMixin

from .models import Vid, VideoMeta
from .forms import VidForm


class VideoMetaInline(admin.TabularInline):
    model = VideoMeta


@admin.register(Vid)
class NativeAdAdmin(admin.ModelAdmin):
    form = VidForm

    list_display = ('name', 'thumb',)
    list_filter = ('categories',)
    search_fields = ['name', 'tags__name']

    inlines = [VideoMetaInline,]

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
        content = ''
        return HttpResponse(content, 'text/html')

    def thumb(self, obj):
        thumbs = obj.videometa.data.get('thumbs', [])

        thumb = 'https://placeholdit.imgix.net/~text?txtsize=18&txt=Generating...&w=128&h=96'
        if thumbs:
            thumb = '%svideo/thumbs-%d-04.jpg' % (settings.MEDIA_URL, obj.pk)
            thumbs = ['%svideo/%s' % (settings.MEDIA_URL, t) for t in thumbs]

        kwargs = {
            'pk': obj.pk,
            'thumb': thumb,
            'url': '%svideo/' % (settings.MEDIA_URL,),
            'thumbs': '["%s"]' % '","'.join(thumbs)
        }
        return mark_safe('<a href="javascript:;" class="view-video" data-pk="{pk}" ><img src="{thumb}" class="slider-thumb" border="0" data-url="{url}" data-images=\'{thumbs}\' /></a>'.format(**kwargs))
    thumb.short_description = 'Thumbnail'

# @admin.register(VideoMeta)
# class VideoMetaAdmin(admin.ModelAdmin): pass
