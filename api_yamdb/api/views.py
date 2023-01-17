from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Category, Genre, Title



class GenresViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass

class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = CatSerializer
    # pagination_class = PageNumberPagination







# def main():
#     with open(.csv) as f:
#         for line in f:
#             process(line)
#     pass
#
# if __name__=='__main__':
#     main()

