# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Vid, VideoMeta
from .forms import VidForm


class VideoMetaInline(admin.TabularInline):
    model = VideoMeta


@admin.register(Vid)
class NativeAdAdmin(admin.ModelAdmin):
    form = VidForm

    list_display = ('name', 'slug', 'thumb',)
    list_filter = ('categories',)
    search_fields = ['name', 'slug', 'tags__name']

    prepopulated_fields = {'slug': ('name',)}
    inlines = [VideoMetaInline,]

    def thumb(self, obj):
        thumbs = obj.videometa.data.get('thumbs', [])
        kwargs = {
          'thumb': '%svideo/thumbs-%d-03.jpg' % (settings.MEDIA_URL, obj.pk),
          'url': '%svideo/' % (settings.MEDIA_URL,),
          'thumbs': ','.join(thumbs)
        }
        return mark_safe('<img src="{thumb}" border="0" data-url="{url}"  data-thumbs="{thumbs}" />'.format(**kwargs))
    thumb.short_description = 'Thumbnail'

# @admin.register(VideoMeta)
# class VideoMetaAdmin(admin.ModelAdmin): pass
