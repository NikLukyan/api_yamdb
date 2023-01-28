import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (Category, Comment, Genre, Review,
                            Title, User, GenreTitle)


def get_reader(file_name: str):
    csv_file_path = os.path.join(settings.CSV_DATA_DIR, file_name)
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        for row in csv.DictReader(csv_file):
            yield row


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories_to_create: list = list()

        for row in get_reader('category.csv'):
            categories_to_create.append(Category(**row))
            Category.objects.bulk_create(categories_to_create, ignore_conflicts=True)
            print('category - OK')

        genres_to_create: list = list()
        for row in get_reader('genre.csv'):
            genres_to_create.append(Genre(**row))
            Genre.objects.bulk_create(genres_to_create, ignore_conflicts=True)
            print('genre - OK')

        titles_to_create: list = list()
        for row in get_reader('titles.csv'):
            titles_to_create.append(Title(**row))
            Title.objects.bulk_create(titles_to_create, ignore_conflicts=True)

            print('titles - OK')







        reviews_to_create: list = list()
        for row in get_reader('review.csv'):
            reviews_to_create.append(Review(**row))
            Review.objects.bulk_create(reviews_to_create, ignore_conflicts=True)

            print('review - OK')

        comments_to_create: list = list()
        for row in get_reader('comments.csv'):
            comments_to_create.append(Comment(**row))
            Comment.objects.bulk_create(comments_to_create, ignore_conflicts=True)

            print('comments - OK')


        genres_title_to_create: list = list()
        for row in get_reader('genre_title.csv'):
            genres_title_to_create.append(GenreTitle(**row))
            GenreTitle.objects.bulk_create(genres_title_to_create, ignore_conflicts=True)

            print('genre_title - OK')

        users_to_create: list = list()
        for row in get_reader('users.csv'):
            users_to_create.append(User(**row))
            User.objects.bulk_create(users_to_create, ignore_conflicts=True)

            print('users - OK')