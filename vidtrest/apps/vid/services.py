# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify
import subprocess

from taggit.models import Tag
from vidtrest.apps.categories.models import VideoCat
#import re
import os


class VideoMetaService(object):
    #cmd = 'ffmpeg -i {video_path} -f ffmetadata'
    cmd = 'exiftool {video_path} > {metadata_path}'

    def __init__(self, pk, video):
        self.pk = pk
        self.video = video

    def process(self):
        tail, head = os.path.split(self.video.path)

        metadata_path = '{path}/{pk}-metadata.txt'.format(path=tail, pk=self.pk)

        cmd = self.cmd.format(video_path=self.video.path,
                              metadata_path=metadata_path)

        subprocess.check_output(cmd, shell=True)

        #
        # Turn exif data into a dict we can use
        #
        meta_data = {}
        with open(metadata_path, 'r') as file:
            for line in file:
                # Split by :
                line_array = line.split(':')
                # First is always the key
                key = line_array[0]
                # everythign else after is always the value
                # rejoin using : again
                val = ':'.join(line_array[1:])
                meta_data[slugify(key.strip())] = val.strip()

        self.meta_data = meta_data

        # If it exists remove it so we can recreate it
        if os.path.isfile(metadata_path):
            os.remove(metadata_path)

        return meta_data


class VideoThumbnailService(object):
    num_thumbs = 5
    thumbs = []
    cmd = 'ffmpeg -ss 3 -i {video_path} -vf "select=gt(scene\,0.2)" -frames:v {num_thumbs} -s 128x96 -vsync vfr {output_path}/thumbs-{pk}-%02d.jpg'

    def __init__(self, pk, video):
        self.pk = pk
        self.video = video

    def process(self):
        tail, head = os.path.split(self.video.path)

        cmd = self.cmd.format(pk=self.pk,
                              num_thumbs=self.num_thumbs,
                              video_path=self.video.path,
                              output_path=tail)

        subprocess.check_output(cmd, shell=True)
        self.thumbs = ['thumbs-%d-%02d.jpg' % (self.pk, i) for i in range(1, self.num_thumbs)]


class ExtractcombinedTagsCategoriesService(object):
    """
    service to extract a field that combines taggit tags and our categories
    and set all of the data as tags, but also save the categories
    """
    def __init__(self, vid, combined_tags):
        if type(combined_tags) not in [set, list, tuple]:
            raise Exception('combined_tags must be a list')

        self.vid = vid

        self.combined_tags = [item.strip() for item in combined_tags]

        self.posted_cats = VideoCat.objects.filter(name__in=self.combined_tags)
        posted_cat_names = [cat.get('name') for cat in self.posted_cats.values()]

        self.posted_tags = [Tag.objects.get_or_create(name=tag)[0] for tag in self.combined_tags if tag not in posted_cat_names]

    def process(self):
        # Delete existing categories
        self.vid.categories.clear()
        # Create the cats
        [self.vid.categories.add(cat) for cat in self.posted_cats]

        # Delete existing tags
        self.vid.tags.clear()
        # Create them
        [self.vid.tags.add(tag) for tag in self.posted_tags]
        return self.vid

