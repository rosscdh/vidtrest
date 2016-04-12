# -*- coding: utf-8 -*-
from django import forms
from dal.forms import FutureModelForm
from taggit.forms import TagField

from .models import Vid


class VidForm(FutureModelForm):
    tags = TagField()

    class Meta:
        model = Vid
        fields = (
            'name',
            'video',
            'tags',
            'categories',
        )
