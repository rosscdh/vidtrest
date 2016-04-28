# -*- coding: UTF-8 -*-
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from model_mommy import mommy

from vidtrest.tests import BaseTestCase
from vidtrest.apps.vid.models import (_thumb_url,
                                      _upload_video,
                                      _validate_file_extension)


class VidModelHelpersTest(BaseTestCase):
    def setUp(self):
        super(VidModelHelpersTest, self).setUp()
        self.vid = mommy.make('vid.Vid',
                              name='Test Video')

    def test_thumb_url(self):
        self.assertEqual(_thumb_url(uuid=self.vid.uuid,
                                    thumb='test-thumb-002.jpg'),
                         u'/media/video/%s/test-thumb-002.jpg' % str(self.vid.uuid))

    def test_upload_video(self):
        self.assertEqual(_upload_video(instance=self.vid,
                                       filename='test-thumb-002.jpg'),
                         u'video/%s/test-thumb-002.jpg' % str(self.vid.uuid))

    def test_validate_file_extension(self):
        class TestObj(object):
            """
            simple placeholder object to contain the file object thats
            referenced in tested method
            """
            file = None

        #
        # Invalid object
        #
        obj = TestObj()

        obj.file = SimpleUploadedFile('file.mp3',
                                      'file_content',
                                      content_type='audio/mp3')

        with self.assertRaises(ValidationError):
            _validate_file_extension(value=obj)

        #
        # Valid object
        #
        obj.file = SimpleUploadedFile('file.mp4',
                                      'file_content',
                                      content_type='video/mp4')

        with self.assertRaises(AssertionError):
            with self.assertRaises(ValidationError):
                _validate_file_extension(value=obj)
