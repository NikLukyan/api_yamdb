import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if value < 1900 or value > dt.datetime.now().year:
        raise ValidationError('Не верно указан год!')
