from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from api.models import Category, Genre, Title
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
    lookup_field = 'slug'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


# def main():
#     with open(.csv) as f:
#         for line in f:
#             process(line)
#     pass
#
# if __name__=='__main__':
#     main()

