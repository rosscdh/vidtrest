# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from jsonfield import JSONField
from taggit.managers import TaggableManager

from vidtrest.apps.utils import managed_s3botostorage, OverwriteStorage

import os
import uuid


def _upload_video(instance, filename):
    split_file_name = os.path.split(filename)[-1]
    filename_no_ext, ext = os.path.splitext(split_file_name)

    full_file_name = '%s%s' % (slugify(filename_no_ext), ext)

    full_path = 'video/%s' % str(instance.uuid)

    return '%s/%s' % (full_path, full_file_name)


def _validate_file_extension(value):
    valid_types = ['video/mp4']
    if value.file.content_type not in valid_types:
        raise ValidationError(u'Please upload a file of type: %s' % ','.join(valid_types))


class Vid(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            db_index=True)

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255,
                                   null=True,
                                   blank=True)

    video = models.FileField(upload_to=_upload_video,
                             storage=OverwriteStorage(),
                             null=True,
                             validators=[_validate_file_extension])
    s3_video = models.FileField(upload_to=_upload_video,
                                storage=managed_s3botostorage(),
                                null=True)

    categories = models.ManyToManyField('categories.VideoCat')

    objects = models.Manager()
    tags = TaggableManager()

    @property
    def thumb(self):
        return self.videometa.thumb

    @property
    def thumbs(self):
        return self.videometa.thumbs

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
        return reverse("vid:detail", kwargs={'pk': self.pk})


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
            thumb = '%svideo/%s/thumbs-04.jpg' % (settings.MEDIA_URL, str(self.vid.uuid))
        return thumb

    @property
    def thumbs(self):
        return mark_safe('["%s"]' % '","'.join(self.thumbs_list()))

    def thumbs_list(self):
        thumbs = self.data.get('thumbs', [])
        return ['%svideo/%s/%s' % (settings.MEDIA_URL, str(self.vid.uuid), t) for t in thumbs]
