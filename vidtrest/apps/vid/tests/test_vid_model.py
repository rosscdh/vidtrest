# -*- coding: UTF-8 -*-
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from model_mommy import mommy

from vidtrest.tests import BaseTestCase
from vidtrest.apps.vid.models import (_thumb_url,
                                      _upload_video,
                                      _validate_file_extension)

import os
FIXTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures')


class VidModelTest(BaseTestCase):
    def setUp(self):
        super(VidModelTest, self).setUp()
        self.vid = mommy.make('vid.Vid',
                              name='Test Video')
        video_file = os.path.join(FIXTURES_DIR, 'ikea_little_dog.mp4')
        with open(video_file) as file:
            uploaded_video_file = SimpleUploadedFile('ikea_little_dog.mp4',
                                                     file.read(),
                                                     content_type='video/mp4')
        self.vid.video = uploaded_video_file
        self.vid.save()
        self.vid.videometa.refresh_from_db()

    def test_get_absolute_url(self):
        self.assertEqual(self.vid.get_absolute_url(), '/vids/{uuid}/'.format(uuid=self.vid.uuid))

    def test_video_upload(self):
        self.assertEqual(self.vid.video.url, '/media/video/%s/ikea_little_dog.mp4' % self.vid.uuid)

    def test_thumb(self):
        self.assertEqual(self.vid.thumb, '/media/video/%s/thumbs-01.jpg' % self.vid.uuid)

    def test_thumbs(self):
        self.assertEqual(self.vid.thumbs, u'["/media/video/{uuid}/thumbs-01.jpg","/media/video/{uuid}/thumbs-02.jpg","/media/video/{uuid}/thumbs-03.jpg","/media/video/{uuid}/thumbs-04.jpg","/media/video/{uuid}/thumbs-05.jpg","/media/video/{uuid}/thumbs-06.jpg","/media/video/{uuid}/thumbs-07.jpg","/media/video/{uuid}/thumbs-08.jpg"]'.format(uuid=str(self.vid.uuid)))

    def test_thumbs_list(self):
        self.assertEqual(type(self.vid.videometa.thumbs_list()), list)
        self.assertEqual(len(self.vid.videometa.thumbs_list()), 8)

    def test_timestamp_thumbs(self):
        self.assertEqual(type(self.vid.videometa.timestamp_thumbs), list)
        self.assertEqual(len(self.vid.videometa.timestamp_thumbs), 8)
        self.assertTrue(len(self.vid.videometa.timestamp_thumbs[0]), 2)

        self.assertEqual(type(self.vid.videometa.timestamp_thumbs[0]), tuple)
        self.assertEqual(self.vid.videometa.timestamp_thumbs[0], (u'/media/video/{uuid}/thumbs-01.jpg'.format(uuid=self.vid.uuid), u'2.04'))
        self.assertEqual(self.vid.videometa.timestamp_thumbs[1], (u'/media/video/{uuid}/thumbs-02.jpg'.format(uuid=self.vid.uuid), u'3.56'))