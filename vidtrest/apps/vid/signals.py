# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import receiver
from django.db.models import signals
from django.core.files.base import ContentFile

from .models import VideoMeta
from .services import VideoMetaService, VideoThumbnailService

from django_rq import job, get_queue
queue = get_queue('high')


@job("default", timeout=72000)
def do_upload_to_s3(instance):
    """
    Upload video file to s3, and then call the following events
    """
    # Ensure we have the latest
    #instance.refresh_from_db()

    # Extract meta-data
    videometa = do_video_meta(instance=instance,
                              video=instance.video)

    if videometa:
        # Extract thumbanils
        do_video_thumbs(instance=instance,
                        video=instance.video)

        if settings.AWS_USE and instance.video:
            instance.s3_video.save(instance.video.path,
                                   ContentFile(instance.video.read()))
            # If we have a s3_video url
            if instance.s3_video.url:
                # Remove the video and refer only to the s3_video
                instance.video.delete()


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

    return videometa.save()


def do_video_thumbs(instance, video):
    videometa, is_new = VideoMeta.objects.get_or_create(vid=instance)

    # Thumbnails
    print ("start video_thumbs")
    service = VideoThumbnailService(pk=instance.pk,
                                    video=instance.video)
    service.process()

    videometa.data.update({
        'thumbs': service.thumbs,
        'thumbs_timestamp': service.thumbs_timestamp,
    })

    videometa.save(update_fields=['data'])


@receiver(signals.post_save,
          sender='vid.Vid',
          dispatch_uid='post_save.get_video_meta')
def post_save_get_video_meta(sender, instance, created, **kwargs):
    """
    Async
    """
    if instance.video:

        if settings.PERFORM_JOBS_SYNCHRONOUSLY is True or settings.PROJECT_ENVIRONMENT in ['test']:
            do_upload_to_s3(instance=instance)
        else:
            queue.enqueue(do_upload_to_s3,
                          instance=instance)
