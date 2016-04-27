# -*- coding: utf-8 -*-
import datetime
from haystack import indexes
from .models import Vid


class VidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    mime_type = indexes.CharField(model_attr='videometa__mime_type')
    duration = indexes.CharField(model_attr='videometa__duration')
    file_size = indexes.CharField(model_attr='videometa__file_size')
    avg_bitrate = indexes.CharField(model_attr='videometa__avg_bitrate')
    audio_sample_rate = indexes.CharField(model_attr='videometa__audio_sample_rate')
    video_frame_rate = indexes.CharField(model_attr='videometa__video_frame_rate')
    audio_bits_per_sample = indexes.CharField(model_attr='videometa__audio_bits_per_sample')
    track_duration = indexes.CharField(model_attr='videometa__track_duration')
    x_resolution = indexes.CharField(model_attr='videometa__x_resolution')
    y_resolution = indexes.CharField(model_attr='videometa__y_resolution')
    file_type = indexes.CharField(model_attr='videometa__file_type')
    audio_format = indexes.CharField(model_attr='videometa__audio_format')
    compressor_id = indexes.CharField(model_attr='videometa__compressor_id')
    image_size = indexes.CharField(model_attr='videometa__image_size')
    image_height = indexes.CharField(model_attr='videometa__image_height')
    image_width = indexes.CharField(model_attr='videometa__image_width')

    def get_model(self):
        return Vid

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.select_related('videometa').all()