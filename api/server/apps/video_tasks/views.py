from celery.result import AsyncResult
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from django.db.models import QuerySet
from django.http import JsonResponse

from server.apps.video_tasks.models import VideoSource
from server.apps.video_tasks.serializers import VideoSourceCreateSerializer, VideoSourceSerializer
from server.apps.video_tasks.tasks import video_retrieve_metadata


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

        video_retrieve_metadata.delay(video_source_id=serializer.instance.pk)

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

    @action(methods=['POST'], detail=False)
    def run_task(self, request: Request, *args, **kwargs) -> JsonResponse:
        tasks = {
            'sample_task_progress': 'server.apps.video_tasks.tasks.sample_task_progress',
        }

        if task_name := request.data.pop('task_name'):
            from celery import current_app

            if celery_task := tasks.get(task_name):
                params = {}
                params.update(request.data.get('params', {}))
                task = current_app.send_task(celery_task, kwargs=params)

                return JsonResponse({'task_id': task.id}, status=202)

            return JsonResponse({'error': 'no such task', 'task_name': task_name}, status=400)

        return JsonResponse({}, status=202)

    @action(methods=['GET'], detail=False)
    def get_task_status(self, request: Request, *args, **kwargs) -> JsonResponse:
        if task_id := request.query_params.get('task_id'):
            task_result = AsyncResult(task_id)
            result = {
                'task_id': task_id,
                'task_result': task_result.result,
                'task_status': task_result.status,
            }
            return JsonResponse(result, status=200)
        return JsonResponse({'r': 'no'}, status=200)
