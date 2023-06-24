# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.urls import reverse
from urllib.parse import urlparse

from taggit.managers import TaggableManager

from vidtrest.apps.utils import managed_s3botostorage, OverwriteStorage

import os
import uuid
import math


def _thumb_url(uuid, thumb):
    url = urlparse(f"{settings.MEDIA_URL}/video/{uuid}/{thumb}")
    return url.geturl()


def _upload_video(instance, filename):
    split_file_name = os.path.split(filename)[-1]
    filename_no_ext, ext = os.path.splitext(split_file_name)

    full_file_name = '%s%s' % (slugify(filename_no_ext), ext)

    full_path = 'video/%s' % str(instance.uuid)

    return '%s/%s' % (full_path, full_file_name)


def _validate_file_extension(value):
    valid_types = ['video/mp4']
    if hasattr(value.file, 'content_type') and value.file.content_type not in valid_types:
        raise ValidationError(u'Please upload a file of type: %s' % ','.join(valid_types))


class Vid(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            db_index=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=128)
    description = models.TextField(null=True)
    video = models.FileField(upload_to=_upload_video,
                             storage=OverwriteStorage(),
                             max_length=500,
                             null=True,
                             blank=True,
                             validators=[_validate_file_extension])
    s3_video = models.FileField(upload_to=_upload_video,
                                storage=managed_s3botostorage(),
                                max_length=500,
                                null=True,
                                blank=True)

    categories = models.ManyToManyField('categories.VideoCat')

    uploaded_by = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, editable=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    objects = models.Manager()
    tags = TaggableManager()

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    @property
    def thumb(self):
        return self.videometa.thumb

    @property
    def thumbs(self):
        return self.videometa.thumbs

    @property
    def preview_thumbs(self):
        return self.videometa.preview_thumbs or '[""]'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_video(self):
        """
        Return the s3_video if its present otherwise the normal one
        """
        if self.s3_video:
            return self.s3_video
        if self.video:
            return self.video
        return None

    def get_absolute_url(self):
        return reverse("vid:detail", kwargs={'uuid': str(self.uuid)})


class VideoMeta(models.Model):
    vid = models.OneToOneField('vid.Vid', on_delete=models.DO_NOTHING)

    mime_type = models.CharField(max_length=24, blank=True, null=True)
    duration = models.CharField(max_length=24, blank=True, null=True)
    file_size = models.CharField(max_length=24, blank=True, null=True)
    avg_bitrate = models.CharField(max_length=24, blank=True, null=True)
    audio_sample_rate = models.CharField(max_length=24, blank=True, null=True)
    video_frame_rate = models.CharField(max_length=24, blank=True, null=True)
    audio_bits_per_sample = models.CharField(max_length=24, blank=True, null=True)
    track_duration = models.CharField(max_length=24, blank=True, null=True)
    x_resolution = models.CharField(max_length=24, blank=True, null=True)
    y_resolution = models.CharField(max_length=24, blank=True, null=True)
    file_type = models.CharField(max_length=24, blank=True, null=True)
    audio_format = models.CharField(max_length=24, blank=True, null=True)
    compressor_id = models.CharField(max_length=24, blank=True, null=True)
    image_size = models.CharField(max_length=24, blank=True, null=True)
    image_height = models.CharField(max_length=24, blank=True, null=True)
    image_width = models.CharField(max_length=24, blank=True, null=True)

    data = models.JSONField(default=dict())

    class Meta:
        verbose_name = "video metadata"
        verbose_name_plural = "video metadata"

    @property
    def image_witdh(self):
        return None

    @property
    def timestamp_thumbs(self):
        thumbs_list = self.thumbs_list()
        times_list = [float(i) + 0.1 for i in self.data.get('thumbs_timestamp', [0 for i in range(0, len(thumbs_list))])]
        times_list.sort()
        return list(zip(thumbs_list,
                        times_list))

    @property
    def thumb(self):
        thumb = 'https://placeholdit.imgix.net/~text?txtsize=18&txt=Generating...&w=128&h=96'
        thumbs = self.thumbs_list()
        if thumbs:
            thumb = thumbs[0]
        return thumb

    @property
    def thumbs(self):
        return mark_safe('["%s"]' % '","'.join(self.thumbs_list()))

    @property
    def preview_thumbs(self):
        """
        capture every n thumbnail from the complete list
        """
        limit = 5
        thumbs_list = self.thumbs_list()
        length_thumbs = len(thumbs_list)

        if length_thumbs <= limit or (length_thumbs / limit) <= limit:
            nth = 1
        else:
            nth = math.ceil(length_thumbs / limit)
            thumbs_list = thumbs_list[::int(nth)]

        limit = math.ceil(len(thumbs_list) / limit)
        if limit > 0:
            thumbs_list = thumbs_list[::int(limit)]

        return mark_safe('["%s"]' % '","'.join(thumbs_list))

    def thumbs_list(self):
        thumbs = self.data.get('thumbs', [])
        thumbs.sort()
        return [_thumb_url(uuid=self.vid.uuid, thumb=t) for t in thumbs]
