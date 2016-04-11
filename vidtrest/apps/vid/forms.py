# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from taggit.forms import TagField, TagWidget

from .models import Vid


class TagsWithKewordsWidget(TagWidget):
    def render(self, name, value, attrs=None):
        html = super(TagsWithKewordsWidget, self).render(name, value, attrs)
        return mark_safe(u'List of keword categories here:<br/> %s' % html)


class VidForm(forms.ModelForm):
    tags = TagField(widget=TagsWithKewordsWidget())

    class Meta:
        model = Vid
        fields = (
            'name',
            'video',
            'tags',
            'categories',
        )
