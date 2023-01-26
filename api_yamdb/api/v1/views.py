from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.confirmation import get_tokens_for_user, send_email
from api.v1.filters import TitleFilter
from api.v1.permissions import (
    AuthorAndStaffOrReadOnly,
    IsAdmin,
    IsAdminOrReadOnly
)
from api.v1.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    JWTTokenAPIViewSerializer,
    ObtainTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class AuthTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if confirmation_code != user.confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUpAPIView(generics.CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, create = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            msg = 'Пользователь с такими данными уже существует'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        send_email(
            serializer.validated_data['email'], confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class JWTTokenAPIView(generics.CreateAPIView):
    """Получение JWT токена для пользователя"""
    serializer_class = JWTTokenAPIViewSerializer
    permission_classes = (AllowAny,)

    def token(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
        )
        if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            token = get_tokens_for_user(user)
            return JsonResponse(
                {'token': token['access']},
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Представление для модели User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
        url_name='me',
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter
    )
    filterset_class = TitleFilter
    search_fields = ['name', 'category', 'slug']

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAndStaffOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                Title,
                id=self.kwargs.get('title_id'),
            ),
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAndStaffOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title, pk=self.kwargs.get("title_id")
        )
        review = get_object_or_404(
            Review, pk=self.kwargs.get("review_id")
        )
        return Comment.objects.filter(
            title=title,
            review=review
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                Title, pk=self.kwargs["title_id"]
            ),
            review=get_object_or_404(
                Review, pk=self.kwargs["review_id"]
            ),
        )
