from rest_framework import permissions, routers

from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from cats.views import AchievementViewSet, CatViewSet, UserViewSet
from trips.views import StopViewSet, TripViewSet

schema_view = get_schema_view(
    openapi.Info(
        title='Kittygram API',
        default_version='v1',
        description='API для управления котиками и их достижениями',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register('cats', CatViewSet)
router.register('users', UserViewSet)
router.register('achievements', AchievementViewSet)
router.register('trips', TripViewSet, basename='trip')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('trips/<int:trip_pk>/stops/',
         StopViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='trip-stops-list'),
    path('trips/<int:trip_pk>/stops/<int:pk>/',
         StopViewSet.as_view({
             'get': 'retrieve', 'put': 'update',
             'patch': 'partial_update', 'delete': 'destroy',
         }),
         name='trip-stops-detail'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
