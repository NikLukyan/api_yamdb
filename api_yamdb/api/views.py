from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from reviews.models import Category, Genre, Title
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer
)


from .serializers import UserSerializer, JWTTokenAPIViewSerializer, SignUpSerializer
from .permissions import IsAdmin
from users.models import User


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title,
                                                pk=self.kwargs["title_id"]))

class UserViewSet(viewsets.ModelViewSet):
    """представление для модели User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    search_fields = ('=username', )
    lookup_field = 'username'
    
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
