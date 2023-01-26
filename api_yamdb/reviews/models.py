from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

from django.db import models

from api.v1.validators import validate_year
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre'),
        verbose_name='Жанр',
        related_name='titles',
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Введите название произведения',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[MinValueValidator(1900),
                    validate_year])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    """Модель отношения Произведение-Жанр"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Отзыв')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author_id', 'title_id'],
                name='unique_review',
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
