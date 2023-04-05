from rest_framework.fields import URLField
from rest_framework.serializers import ModelSerializer

from server.apps.video_tasks.models import VideoSource


class VideoSourceCreateSerializer(ModelSerializer):
    url = URLField(max_length=255, required=True)

    class Meta:
        model = VideoSource
        fields = ('id', 'url', 'user')
        read_only_fields = ('id',)

    def create(self, validated_data: dict) -> VideoSource:
        # name = validated_data.get('name')
        # validated_data['name'] = name or validated_data['file'].name
        return super().create(validated_data)


class VideoSourceSerializer(ModelSerializer):
    class Meta:
        model = VideoSource
        fields = '__all__'
