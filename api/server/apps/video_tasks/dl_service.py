from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import yt_dlp
from pytz import utc

from django.conf import settings
from django.core.files import File
from django.db import IntegrityError

from server.apps.video_tasks.models import VideoSource


class VideoMetadata(TypedDict):
    extractor: int
    id: str
    title: str
    channel: str
    uploader_id: str
    duration: int
    thumbnail: str
    webpage_url: str
    timestamp: int
    upload_date: str


@contextmanager
def cd(path: Path) -> None:
    """
    change current directory with cm
    """
    cwd = Path.cwd()
    os.chdir(path)
    yield
    os.chdir(cwd)


class VideoDlService:
    @staticmethod
    def get_metadata(video_url: str) -> VideoMetadata:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return VideoMetadata(**ydl.sanitize_info(info))

    @staticmethod
    def fill_metadata(video_source: VideoSource, metadata: VideoMetadata) -> VideoSource:
        video_source.extractor = metadata.get('extractor', '')
        video_source.source_id = metadata.get('id', '')
        video_source.title = metadata.get('title', '')
        video_source.channel = metadata.get('channel', '')
        video_source.uploader_id = metadata.get('uploader_id', '')
        video_source.duration = metadata.get('duration', 0)
        video_source.thumbnail = metadata.get('thumbnail', '')
        video_source.url = metadata.get('webpage_url', '')

        if timestamp := metadata.get('timestamp'):
            video_source.upload_date = datetime.fromtimestamp(timestamp, tz=utc)
        elif date := metadata.get('upload_date'):
            video_source.upload_date = datetime.strptime(date, '%Y%m%d').replace(tzinfo=utc).date()
        try:
            video_source.save()
        except IntegrityError:
            video_source_del = video_source
            video_source = VideoSource.objects.get(
                source_id=video_source.source_id,
                extractor=video_source.extractor,
            )
            if video_source:
                video_source_del.delete()
        return video_source

    @staticmethod
    def download_audio(video_url: str, name: str = '') -> Path | None:
        codec = 'mp3'  # m4a
        name = name.split('.')[0]
        # ext_file_name = name or '%(id)s.%(ext)s'
        ext_file_name = name or 'extracted_audio'

        ydl_opts = {
            'format': f'{codec}/bestaudio/best',
            'outtmpl': ext_file_name,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': codec,
                }
            ],
        }

        with (
            cd(settings.FILE_UPLOAD_TEMP_DIR),
            yt_dlp.YoutubeDL(ydl_opts) as ydl,
        ):
            error_code = ydl.download(video_url)

        if not error_code:
            return Path(settings.FILE_UPLOAD_TEMP_DIR / f'{ext_file_name}.{codec}')

        return None

    @staticmethod
    def store_audio(video_source: VideoSource, file_path: Path) -> None:
        if video_source.file.name:
            return

        with file_path.open(mode='rb') as f:
            video_source.file = File(f, name=file_path.name)
            video_source.file_size = video_source.file.size
            video_source.save(update_fields=('file', 'file_size'))
