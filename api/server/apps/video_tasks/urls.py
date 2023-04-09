from rest_framework import routers

from django.urls import include, path

from server.apps.video_tasks.views import VideoSourceModelViewSet

app_name = 'video_tasks'

router = routers.DefaultRouter()
router.register('', VideoSourceModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
