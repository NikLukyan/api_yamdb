from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (TitlesViewSet,
                       GenresViewSet,
                       CategoryViewSet,
                       ReviewViewSet)
from .views import SignUpAPIView, JWTTokenAPIView, UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register('titles', TitlesViewSet, basename='titles')
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router.register('users', UserViewSet, basename='users')



urlpatterns = [
    path('v1/', include(router.urls), name='api_v1'),
    path('v1/auth/signup/', SignUpAPIView.as_view()),
    path('v1/auth/token/', JWTTokenAPIView.as_view()),
]
