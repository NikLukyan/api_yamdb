from django.contrib.auth import get_user_model
from django.db import models
from api.validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre)
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название произведения'
    )
    year = models.IntegerField(
        verbose_name='год выпуска произведения',
        validators=[validate_year])

    def __str__(self):
        return self.name


# def main():
#     with open .csv

#
# if request.user.is_authenticated:
#     return