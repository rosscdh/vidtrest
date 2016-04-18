# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

from jsonfield import JSONField
from taggit.managers import TaggableManager

from vidtrest.apps.utils import managed_s3botostorage, OverwriteStorage

import os
#import uuid


def _upload_video(instance, filename):
    split_file_name = os.path.split(filename)[-1]
    filename_no_ext, ext = os.path.splitext(split_file_name)

    full_file_name = '%s%s' % (slugify(filename_no_ext), ext)

    full_path = 'video/%s/%s' % (instance.pk, full_file_name)
    #import pdb;pdb.set_trace()
    try:
        os.makedirs(full_path)
    except OSError as e:
        if e.errno == 17:
            # Dir already exists. No biggie.
            pass

    return full_path


class Vid(models.Model):
    name = models.CharField(max_length=255)

    video = models.FileField(upload_to=_upload_video,
                             storage=OverwriteStorage(),
                             null=True)
    s3_video = models.FileField(upload_to=_upload_video,
                                storage=managed_s3botostorage(),
                                null=True)

    categories = models.ManyToManyField('categories.VideoCat')

    objects = models.Manager()
    tags = TaggableManager()

    def get_video(self):
        """
        Return the s3_video if its present otherwise the normal one
        """
        if self.s3_video:
            return self.s3_video
        if self.video:
            return self.video
        return None

    @property
    def thumb(self):
        return self.videometa.thumb

    @property
    def thumbs(self):
        return self.videometa.thumbs


class VideoMeta(models.Model):
    vid = models.OneToOneField('vid.Vid')

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

    data = JSONField(default={})

    @property
    def thumb(self):
        thumb = 'https://placeholdit.imgix.net/~text?txtsize=18&txt=Generating...&w=128&h=96'
        thumbs = self.data.get('thumbs', [])
        if thumbs:
            thumb = '%svideo/%s/thumbs-%d-04.jpg' % (settings.MEDIA_URL, self.vid.pk, self.vid.pk)
        return thumb

    @property
    def thumbs(self):
        thumbs = self.data.get('thumbs', [])
        thumbs = ['%svideo/%s/%s' % (settings.MEDIA_URL, self.vid.pk, t) for t in thumbs]
        return '["%s"]' % '","'.join(thumbs)
