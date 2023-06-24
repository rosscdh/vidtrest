# Generated by Django 4.2.2 on 2023-06-23 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid
import vidtrest.apps.utils
import vidtrest.apps.vid.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("categories", "0002_alter_videocat_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vid",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(allow_unicode=True, max_length=128)),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        max_length=500,
                        null=True,
                        storage=vidtrest.apps.utils.OverwriteStorage(),
                        upload_to=vidtrest.apps.vid.models._upload_video,
                        validators=[vidtrest.apps.vid.models._validate_file_extension],
                    ),
                ),
                (
                    "s3_video",
                    models.FileField(
                        blank=True,
                        max_length=500,
                        null=True,
                        storage=vidtrest.apps.utils.OverwriteStorage(),
                        upload_to=vidtrest.apps.vid.models._upload_video,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                ("categories", models.ManyToManyField(to="categories.videocat")),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "video",
                "verbose_name_plural": "videos",
            },
        ),
        migrations.CreateModel(
            name="VideoMeta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mime_type", models.CharField(blank=True, max_length=24, null=True)),
                ("duration", models.CharField(blank=True, max_length=24, null=True)),
                ("file_size", models.CharField(blank=True, max_length=24, null=True)),
                ("avg_bitrate", models.CharField(blank=True, max_length=24, null=True)),
                (
                    "audio_sample_rate",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                (
                    "video_frame_rate",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                (
                    "audio_bits_per_sample",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                (
                    "track_duration",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                (
                    "x_resolution",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                (
                    "y_resolution",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                ("file_type", models.CharField(blank=True, max_length=24, null=True)),
                (
                    "audio_format",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                (
                    "compressor_id",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                ("image_size", models.CharField(blank=True, max_length=24, null=True)),
                (
                    "image_height",
                    models.CharField(blank=True, max_length=24, null=True),
                ),
                ("image_width", models.CharField(blank=True, max_length=24, null=True)),
                ("data", models.JSONField(default={})),
                (
                    "vid",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="vid.vid"
                    ),
                ),
            ],
            options={
                "verbose_name": "video metadata",
                "verbose_name_plural": "video metadata",
            },
        ),
    ]