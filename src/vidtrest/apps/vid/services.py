# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify
from django.core.files.storage import default_storage

from taggit.models import Tag
from vidtrest.apps.categories.models import VideoCat
from vidtrest.apps.utils import managed_s3botostorage

import os
import glob
import subprocess
import logging

logger = logging.getLogger(__name__)


class VideoMetaService(object):
    cmd = 'exiftool {video_path} > {metadata_path}'

    def __init__(self, pk, video):
        self.pk = pk
        self.video = video

    def process(self):
        tail, head = os.path.split(self.video.path)

        metadata_path = '{path}/metadata.txt'.format(path=tail)

        cmd = self.cmd.format(video_path=self.video.path,
                              metadata_path=metadata_path)
        logger.info(f"exif command: {cmd}")
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
        # if os.path.isfile(metadata_path):
        #     os.remove(metadata_path)

        return meta_data


class VideoThumbnailService(object):
    num_thumbs = 10
    output_path = None
    thumbs = []
    thumbs_timestamp = {}

    #cmd = 'ffmpeg -ss 3 -i {video_path} -vf "select=gt(scene\,0.3)" -s 320x200 -vsync vfr {output_path}/thumbs-%02d.jpg'
    cmd = "ffmpeg -i {video_path} -r 25 -s 320x200 -vsync passthrough -pix_fmt yuvj422p -an -vf select='gt(scene\,0.7)',showinfo {output_path}/thumbs-%02d.jpg -f null - 2>&1 | grep 'pts_time' | awk -F'pts_time:' '{{print $2}}' | awk -F'pos:' '{{print $1}}' > {output_path}/thumbs_timestamp.txt"
    #cmd = "ffmpeg --opengl-early-flush=no -i {video_path} -vprofile baseline -vcodec libx264 -r 40 -bt 5K -s 960x540 -ac 2 -ar 48000 -ab 192k -strict -2 -y -vf select='gt(scene\,0.4)',showinfo {output_path}/thumbs-%02d.jpg -f null - 2>&1 | grep 'pts_time' | awk -F'pts_time:' '{{print $2}}' | awk -F'pos:' '{{print $1}}' > {output_path}/thumbs_timestamp.txt"

    def __init__(self, pk, video):
        self.pk = pk
        self.video = video

    def upload_thumbs(self, thumbs=[]):
        if thumbs:
            storage = managed_s3botostorage()
            for thumb in thumbs:
                file_path = os.path.join(self.output_path, thumb)
                if os.path.exists(file_path):
                    s3_file_path = '%s' % '/'.join(file_path.split('/')[-3:])
                    logger.debug(f"Upload to: {s3_file_path}")
                    storage.save(s3_file_path, default_storage.open(file_path))
        return thumbs

    def upload_video(self, video):
        if video:
            storage = managed_s3botostorage()
            file_path = os.path.join(self.output_path, video)
            if os.path.exists(file_path):
                s3_file_path = '%s' % '/'.join(file_path.split('/')[-3:])
                logger.debug(f"Upload to: {s3_file_path}")
                storage.save(s3_file_path, default_storage.open(file_path))
        return video

    def process(self):
        self.output_path, head = os.path.split(self.video.path)

        cmd = self.cmd.format(pk=self.pk,
                              num_thumbs=self.num_thumbs,
                              video_path=self.video.path,
                              output_path=self.output_path)

        with open(os.devnull, 'w') as devnull:
            print(cmd)
            subprocess.check_output(cmd, shell=True, stderr=devnull)

        #
        # Timestamps range
        #
        timerange_path = '%s/thumbs_timestamp.txt' % self.output_path
        thumbs_timestamp = [line.strip() for line in open(timerange_path, 'r')]
        self.thumbs_timestamp = thumbs_timestamp
        #
        # Thumbnails
        #
        list_thumbs = glob.glob('{output_path}/*.jpg'.format(output_path=self.output_path))
        list_thumbs = [os.path.split(t)[1] for t in list_thumbs]
        self.thumbs = self.upload_thumbs(thumbs=list_thumbs)
        self.upload_video(video=self.video.path)


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

