from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import (
    IsAdmin,
    IsAdminUserOrReadOnly,
    IsAuthorOrAdminOrModeratorOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    JWTTokenAPIViewSerializer,
    ProfileSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
)
from api.confirmation import get_tokens_for_user, send_email
from reviews.models import Category, Comment, Genre, Review, Title
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'slug']

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return Review.objects.filter(title=title)  # title.reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title,
                                                pk=self.kwargs["title_id"]))


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return Comment.objects.filter(title=title, review=review)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title,
                                                pk=self.kwargs["title_id"]),
                        review=get_object_or_404(Review,
                                                 pk=self.kwargs["review_id"])
                        )


class UserViewSet(viewsets.ModelViewSet):
    """представление для модели User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    search_fields = ('username', )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    
    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
        serializer_class=ProfileSerializer
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
    serializer_class = JWTTokenAPIViewSerializer
    permission_classes = (AllowAny,)

    def token(request):
        serializer = JWTTokenAPIViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
        )
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']):
            token = get_tokens_for_user(user)
            return JsonResponse(
                {'token': token['access']},
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SignUpAPIView(APIView):
    """регистрация пользователя"""
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            msg = 'Пользователь с такими данными уже существует'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        send_email(serializer.validated_data['email'], confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)
