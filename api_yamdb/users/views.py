from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from users.models import User
from users.serializers import UserSerializer, JWTTokenAPIViewSerializer


class SingUpAPIView(APIView):
    """регистрация пользователя"""
    pass
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    """представление для модели User"""
    serialiser_class = UserSerializer
    queryset = User.objects.all()


class JWTTokenAPIView(APIView):
    """получение JWT токена для пользователя"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = JWTTokenAPIViewSerializer(data=self.request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
