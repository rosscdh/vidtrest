# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify
import subprocess

import re
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