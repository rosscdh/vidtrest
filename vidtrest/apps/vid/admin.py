# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
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

    def thumb(self, obj):
        thumbs = obj.videometa.data.get('thumbs', [])

        thumb = 'https://placeholdit.imgix.net/~text?txtsize=18&txt=Generating...&w=128&h=96'
        if thumbs:
            thumb = '%svideo/thumbs-%d-04.jpg' % (settings.MEDIA_URL, obj.pk)
            thumbs = ['%svideo/%s' % (settings.MEDIA_URL, t) for t in thumbs]

        kwargs = {
            'thumb': thumb,
            'url': '%svideo/' % (settings.MEDIA_URL,),
            'thumbs': '["%s"]' % '","'.join(thumbs)
        }
        return mark_safe('<img src="{thumb}" class="slider-thumb" border="0" data-url="{url}" data-images=\'{thumbs}\' />'.format(**kwargs))
    thumb.short_description = 'Thumbnail'

# @admin.register(VideoMeta)
# class VideoMetaAdmin(admin.ModelAdmin): pass
