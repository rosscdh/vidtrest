# -*- coding: utf-8 -*-
#import datetime
from haystack import indexes
from .models import VideoMeta


class VidIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='vid__name')
    uuid = indexes.CharField(model_attr='vid__uuid')
    mime_type = indexes.CharField(model_attr='mime_type', null=True)
    duration = indexes.CharField(model_attr='duration', null=True)
    file_size = indexes.CharField(model_attr='file_size', null=True)
    avg_bitrate = indexes.CharField(model_attr='avg_bitrate', null=True)
    audio_sample_rate = indexes.CharField(model_attr='audio_sample_rate', null=True)
    video_frame_rate = indexes.CharField(model_attr='video_frame_rate', null=True)
    audio_bits_per_sample = indexes.CharField(model_attr='audio_bits_per_sample', null=True)
    track_duration = indexes.CharField(model_attr='track_duration', null=True)
    x_resolution = indexes.CharField(model_attr='x_resolution', null=True)
    y_resolution = indexes.CharField(model_attr='y_resolution', null=True)
    file_type = indexes.CharField(model_attr='file_type', null=True)
    audio_format = indexes.CharField(model_attr='audio_format', null=True)
    compressor_id = indexes.CharField(model_attr='compressor_id', null=True)
    image_size = indexes.CharField(model_attr='image_size', null=True)
    image_height = indexes.CharField(model_attr='image_height', null=True)
    image_width = indexes.CharField(model_attr='image_width', null=True)

    def get_model(self):
        return VideoMeta

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.select_related('vid').all()