# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver

from .models import VideoMeta
from .services import VideoMetaService, VideoThumbnailService

import django_rq
queue = django_rq.get_queue('high')


def do_upload_to_s3(instance):
    """
    Upload video file to s3, and then call the following events
    """
    if settings.AWS_STORAGE_BUCKET_NAME:
        instance.s3_video.save(instance.video.name, instance.video.read())
        instance.save(update_fields=['s3_video'])

    # Extract meta-data
    do_video_meta(instance=instance,
                  video=instance.video)

    # Extract thumbanils
    do_video_thumbs(instance=instance,
                    video=instance.video)

    # Delete original video if its been handed off too s3
    if settings.AWS_STORAGE_BUCKET_NAME and instance.s3_video:
        instance.video.delete()
        instance.save(update_fields=['video'])


def do_video_meta(instance, video):
    videometa, is_new = VideoMeta.objects.get_or_create(vid=instance)

    service = VideoMetaService(pk=instance.pk,
                               video=instance.video)
    service.process()

    videometa.data.update({'video_metadata': service.meta_data})

    videometa.mime_type = service.meta_data.get('mime-type')
    videometa.duration = service.meta_data.get('duration')
    videometa.file_size = service.meta_data.get('file-size')
    videometa.avg_bitrate = service.meta_data.get('avg-bitrate')
    videometa.audio_sample_rate = service.meta_data.get('audio-sample-rate')
    videometa.video_frame_rate = service.meta_data.get('video-frame-rate')
    videometa.audio_bits_per_sample = service.meta_data.get('audio-bits-per-sample')
    videometa.track_duration = service.meta_data.get('track-duration')
    videometa.x_resolution = service.meta_data.get('x-resolution')
    videometa.y_resolution = service.meta_data.get('y-resolution')
    videometa.file_type = service.meta_data.get('file-type')
    videometa.audio_format = service.meta_data.get('audio-format')
    videometa.compressor_id = service.meta_data.get('compressor-id')
    videometa.image_size = service.meta_data.get('image-size')
    videometa.image_height = service.meta_data.get('image-height')
    videometa.image_width = service.meta_data.get('image-width')

    videometa.save()


def do_video_thumbs(instance, video):
    videometa, is_new = VideoMeta.objects.get_or_create(vid=instance)
    # Thumbnails
    service = VideoThumbnailService(pk=instance.pk,
                                    video=instance.video)
    service.process()
    videometa.data.update({'thumbs': service.thumbs})
    videometa.save(update_fields=['data'])


@receiver(signals.post_save,
          sender='vid.Vid',
          dispatch_uid='post_save.get_video_meta')
def post_save_get_video_meta(sender, instance, created, **kwargs):
    """
    Async
    """
    if instance.video:
        queue.enqueue(do_upload_to_s3,
                      instance=instance)
