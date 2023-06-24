# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from storages.backends.s3boto3 import S3Boto3Storage


class VideoMediaStorage(S3Boto3Storage):
    location = ""
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL')
    default_acl = "public-read"
    file_overwrite = True


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def managed_s3botostorage():
    if settings.AWS_USE is True:
        return VideoMediaStorage()
    else:
        return OverwriteStorage()
