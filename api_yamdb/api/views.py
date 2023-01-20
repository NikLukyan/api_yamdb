from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
    # PageNumberPagination
from reviews.models import Category, Genre, Title
from rest_framework import filters
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # filter_backends = [filters.SearchFilter]
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

