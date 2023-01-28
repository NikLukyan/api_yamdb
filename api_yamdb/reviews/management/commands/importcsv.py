import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, Review,
                            Title, User, GenreTitle)

# ВАРИАНТ 1

DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}

REPLACE_FIELDS = {
    Title: ['category', 'category_id'],
    Review: ['author', 'author_id'],
    Comment: ['author', 'author_id'],
}


def get_reader(file_name: str):
    csv_file_path = os.path.join(settings.CSV_DATA_DIR, file_name)
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        for row in csv.DictReader(csv_file):
            yield row


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, base in DATA.items():
            csv_file_path = os.path.join(settings.CSV_DATA_DIR, base)
            with open(
                    csv_file_path, 'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if model in REPLACE_FIELDS:
                        row[REPLACE_FIELDS[model][1]] = row.pop(
                            REPLACE_FIELDS[model][0])
                    model.objects.create(**row)

# ВАРИАНТ 2
#
# def get_reader(file_name: str):
#     csv_file_path = os.path.join(settings.CSV_DATA_DIR, file_name)
#     with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
#         for row in csv.DictReader(csv_file):
#             yield row
#
# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#
#         categories_to_create: list = list()
#         for row in get_reader('category.csv'):
#             categories_to_create.append(Category(**row))
#             Category.objects.bulk_create(categories_to_create, ignore_conflicts=True)
#
#         genres_to_create: list = list()
#         for row in get_reader('genre.csv'):
#             genres_to_create.append(Genre(**row))
#             Genre.objects.bulk_create(genres_to_create, ignore_conflicts=True)
#
#         titles_to_create: list = list()
#         for row in get_reader('titles.csv'):
#             row['category_id'] = row.pop('category')
#             titles_to_create.append(Title(**row))
#             Title.objects.bulk_create(titles_to_create, ignore_conflicts=True)
#
#         reviews_to_create: list = list()
#         for row in get_reader('review.csv'):
#             row['author_id'] = row.pop('author')
#             reviews_to_create.append(Review(**row))
#             Review.objects.bulk_create(reviews_to_create, ignore_conflicts=True)
#
#         comments_to_create: list = list()
#         for row in get_reader('comments.csv'):
#             row['author_id'] = row.pop('author')
#             comments_to_create.append(Comment(**row))
#             Comment.objects.bulk_create(comments_to_create, ignore_conflicts=True)
#
#         genres_title_to_create: list = list()
#         for row in get_reader('genre_title.csv'):
#             genres_title_to_create.append(GenreTitle(**row))
#             GenreTitle.objects.bulk_create(genres_title_to_create, ignore_conflicts=True)
#
#         users_to_create: list = list()
#         for row in get_reader('users.csv'):
#             users_to_create.append(User(**row))
#             User.objects.bulk_create(users_to_create, ignore_conflicts=True)
