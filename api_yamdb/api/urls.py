from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (TitlesViewSet,
                       GenresViewSet,
                       CategoryViewSet,
                       ReviewViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('titles', TitlesViewSet, basename='titles')
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='review')


urlpatterns = [
    path('v1/', include(router.urls), name='api_v1'),
    path('v1/auth/token', include('djoser.urls.jwt')),
]
