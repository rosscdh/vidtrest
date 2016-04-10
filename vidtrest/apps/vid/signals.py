# -*- coding: utf-8 -*-
from django.db.models import signals
from django.dispatch import receiver

import django_rq
queue = django_rq.get_queue('high')


from .models import VideoMeta
from .services import VideoMetaService, VideoThumbnailService


def do_video_meta(instance, video):
    videometa, is_new = VideoMeta.objects.get_or_create(vid=instance)

    service = VideoMetaService(pk=instance.pk,
                               video=instance.video)
    service.process()

    videometa.data.update(service.meta_data)
    videometa.save()


def do_video_thumbs(instance, video):
    #videometa, is_new = VideoMeta.objects.get_or_create(vid=instance)
    # Thumbnails
    service = VideoThumbnailService(pk=instance.pk,
                                    video=instance.video)
    service.process()


@receiver(signals.post_save,
          sender='vid.Vid',
          dispatch_uid='post_save.get_video_meta')
def post_save_get_video_meta(sender, instance, created, **kwargs):
    """
    Async
    """
    if instance.video:
        queue.enqueue(do_video_meta, instance=instance, video=instance.video)
        queue.enqueue(do_video_thumbs, instance=instance, video=instance.video)
