from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (TitlesViewSet, GenresViewSet, CategoryViewSet)

router = DefaultRouter()

router.register('titles', TitlesViewSet, basename='titles')
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token', include('djoser.urls.jwt')),
]
