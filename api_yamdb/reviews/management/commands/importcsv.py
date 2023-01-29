import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, Review,
                            Title, User, GenreTitle)


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
