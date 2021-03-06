# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 04:48
from __future__ import unicode_literals

from django.db import migrations, models
import storages.backends.s3boto
import vidtrest.apps.utils
import vidtrest.apps.vid.models


class Migration(migrations.Migration):

    dependencies = [
        ('vid', '0005_auto_20160420_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vid',
            name='s3_video',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto.S3BotoStorage(), upload_to=vidtrest.apps.vid.models._upload_video),
        ),
        migrations.AlterField(
            model_name='vid',
            name='video',
            field=models.FileField(blank=True, null=True, storage=vidtrest.apps.utils.OverwriteStorage(), upload_to=vidtrest.apps.vid.models._upload_video, validators=[vidtrest.apps.vid.models._validate_file_extension]),
        ),
    ]
