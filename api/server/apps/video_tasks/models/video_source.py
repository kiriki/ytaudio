from __future__ import annotations

import pathlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, URLField, UniqueConstraint


def upload_directory_path(instance: VideoSource, filename: str) -> str:
    extension = pathlib.Path(filename).suffix
    filename = f'{instance.channel} - {instance.title} {instance.source_id}'
    return f'user/dir/{filename}{extension}'


class VideoSource(models.Model):
    url = URLField(max_length=255)
    added_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # metadata
    source_id = models.CharField(blank=True)
    extractor = models.CharField(max_length=50, blank=True)
    title = models.CharField(blank=True)
    channel = models.CharField(blank=True)
    uploader_id = models.CharField(blank=True)
    duration = models.PositiveSmallIntegerField(default=0)
    upload_date = models.DateField(default='1900-01-01')
    thumbnail = URLField(max_length=255, blank=True)
    info = models.JSONField(default=dict)

    # media
    file = models.FileField(max_length=255, null=True, upload_to=upload_directory_path)
    file_size = models.IntegerField(null=True)

    class Meta:
        ordering = ['-added_date']
        constraints = [
            UniqueConstraint(
                fields=['source_id', 'extractor'],
                name='unique_source_id_extractor',
                condition=~Q(title=''),
            ),
        ]

    def __str__(self) -> str:
        return f'Video(pk={self.pk}) {self.url}'
