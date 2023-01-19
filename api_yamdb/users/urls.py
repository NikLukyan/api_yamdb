from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import JWTTokenAPIView, SingUpAPIView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SingUpAPIView.as_view()),
    path('v1/auth/token/', JWTTokenAPIView.as_view()),
    path('v1/', include(router.urls)),
]
