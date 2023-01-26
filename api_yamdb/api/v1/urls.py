from django.urls import include, path
from rest_framework import routers

from api.v1.views import AuthTokenView as Auth
from api.v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    SignUpAPIView,
    TitlesViewSet,
    UserViewSet,
)

auth_urls = [
    path(r'token/', Auth.as_view(), name='auth'),
    path(r'signup/', SignUpAPIView.as_view(), name='signup'),
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
    path('', include(router.urls)),
    path(r'auth/', include(auth_urls)),
]