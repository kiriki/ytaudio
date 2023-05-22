"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from server.apps.users.sample_view import index_test
from server.apps.users.views import LoginView, LogoutView, UserViewSet
from server.apps.video_tasks.views import VideoSourceModelViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet)
router.register('tasks', VideoSourceModelViewSet)

urlpatterns = [
    path('', index_test),
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'api'))),
    # path('api/rest/', include('video_tasks.urls', namespace='api')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += [
    path('api/auth/login/', LoginView.as_view()),
    path('api/auth/logout/', LogoutView.as_view()),
    path('api/auth1/', include('rest_framework.urls', namespace='rest_framework')),
]

# path('schema/', get_schema_view(title='Q Site API')),
# path('docs/', include_docs_urls(title='Q Site API service')),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
