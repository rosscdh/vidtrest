# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class VidConfig(AppConfig):
    name = 'vidtrest.apps.vid'
    verbose_name = 'Videos'

    def ready(self):
        from vidtrest.apps.vid.signals import post_save_get_video_meta
