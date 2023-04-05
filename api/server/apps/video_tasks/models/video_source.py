from django.contrib.auth.models import User
from django.db import models
from django.db.models import URLField


class VideoSource(models.Model):
    url = URLField(max_length=255)
    added_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-added_date']

    def __str__(self) -> str:
        return f'Video(pk={self.pk}) {self.url}'
