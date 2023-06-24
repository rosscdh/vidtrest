# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class VideoCat(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
