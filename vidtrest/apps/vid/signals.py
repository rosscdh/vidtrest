# -*- coding: utf-8 -*-
from django.db.models import signals
from django.dispatch import receiver
from .models import VideoMeta
from .services import VideoMetaService



@receiver(signals.post_save,
          sender='vid.Vid',
          dispatch_uid='post_save.get_video_meta')
def post_save_get_video_meta(sender, instance, **kwargs):
    if instance.video:  # created
        service = VideoMetaService(video=instance.video)
        service.process()

        videometa, is_new = VideoMeta.objects.get_or_create(vid=instance)

        videometa.data.update(service.meta_data)
        videometa.save()
