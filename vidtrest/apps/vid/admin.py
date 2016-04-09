# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Vid, VideoMeta
from .forms import VidForm


class VideoMetaInline(admin.TabularInline):
    model = VideoMeta


@admin.register(Vid)
class NativeAdAdmin(admin.ModelAdmin):
    form = VidForm

    search_fields = ['slug', 'name', 'tags']
    list_display = ('slug', 'name',)

    prepopulated_fields = {'slug': ('name',)}
    inlines = [VideoMetaInline,]


# @admin.register(VideoMeta)
# class VideoMetaAdmin(admin.ModelAdmin): pass
