from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenresViewSet,
    JWTTokenAPIView,
    ReviewViewSet,
    SignUpAPIView,
    TitlesViewSet,
    UserViewSet,
)

auth_urls = [
    path(r'token/', JWTTokenAPIView.as_view()),
    path(r'signup/', SignUpAPIView.as_view()),
]

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(r'v1/auth/', include(auth_urls)),
]
