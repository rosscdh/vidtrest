# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

from jsonfield import JSONField
#from s3direct.fields import S3DirectField
from taggit.managers import TaggableManager

from vidtrest.apps.utils import managed_s3botostorage

import os
import uuid


def _upload_video(instance, filename):
    split_file_name = os.path.split(filename)[-1]
    filename_no_ext, ext = os.path.splitext(split_file_name)

    pk = str(uuid.uuid4())
    pk = pk.split('-')[0]
    identifier = '%s-%s' % (instance.slug, pk)
    full_file_name = '%s-%s%s' % (identifier, slugify(filename_no_ext), ext)

    return 'video/%s' % full_file_name


class Vid(models.Model):
    name = models.CharField(max_length=255)

    #video = S3DirectField(dest='vids', null=True)
    video = models.FileField(upload_to=_upload_video,
                             storage=managed_s3botostorage(),
                             null=True)

    categories = models.ManyToManyField('categories.VideoCat')

    objects = models.Manager()
    tags = TaggableManager()


class VideoMeta(models.Model):
    vid = models.OneToOneField('vid.Vid')
    data = JSONField(default={})