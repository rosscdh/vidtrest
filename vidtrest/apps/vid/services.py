# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify
import subprocess

import re
import os


class VideoMetaService(object):
    #cmd = 'ffmpeg -i {video_path} -f ffmetadata'
    cmd = 'exiftool {video_path} > {metadata_path}'

    def __init__(self, video):
        self.video = video

    def process(self):
        tail, head = os.path.split(self.video.path)

        metadata_path = '{path}/meta_data.txt'.format(path=tail)

        # If it exists remove it so we can recreate it
        if os.path.isfile(metadata_path):
            os.remove(metadata_path)

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

        return meta_data
