from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from django.db.models import QuerySet

from server.apps.video_tasks.models import VideoSource
from server.apps.video_tasks.serializers import VideoSourceCreateSerializer, VideoSourceSerializer


class VideoSourceModelViewSet(ModelViewSet):
    queryset = VideoSource.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return self.queryset.all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # app_config.service.send_to_controller(RenameFileRequest(id=serializer.instance.pk))

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        return Response(data=pk, status=status.HTTP_202_ACCEPTED)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == 'POST':
            return VideoSourceCreateSerializer
        return VideoSourceSerializer
