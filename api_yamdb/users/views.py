from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from users.models import User
from users.serializers import SignUpSerializer, UserSerializer, JWTTokenAPIViewSerializer
from users.permissions import IsAdmin


class SignUpAPIView(APIView):
    """регистрация пользователя"""
    permission_classes = (AllowAny,)

    def signup(request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, _ = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            '',
            confirmation_code,
            settings.EMAIL_ADMIN,
            [email],
            fail_silently=False
        )
        response = {
            'email': email,
            'username': username
        }
        return Response(response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """представление для модели User"""
    serialiser_class = UserSerializer
    permission_classes = (IsAdmin, )
    search_fields = ('=username', )
    lookup_field = 'username'
    queryset = User.objects.all()
    
    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        data = request.data
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class JWTTokenAPIView(APIView):
    """получение JWT токена для пользователя"""
    permission_classes = (AllowAny,)

    def token(request):
        serializer = JWTTokenAPIViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            access_token = RefreshToken.for_user(user)
            response = {'token': str(access_token.access_token)}
            return Response(response, status=status.HTTP_200_OK)
        response = {user.username: 'Confirmation code incorrect.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

