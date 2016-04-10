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
    search_fields = ['name', 'slug', 'tags']

    prepopulated_fields = {'slug': ('name',)}
    inlines = [VideoMetaInline,]

    def thumb(self, obj):
        kwargs = {
          'thumb': '%svideo/%d-thumb-06.jpg' % (settings.MEDIA_URL, obj.pk)
        }
        return mark_safe('<img src="{thumb}" border="0" />'.format(**kwargs))
    thumb.short_description = 'Thumbnail'

# @admin.register(VideoMeta)
# class VideoMetaAdmin(admin.ModelAdmin): pass
