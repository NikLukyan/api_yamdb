from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]

class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Логин пользователя',
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        verbose_name='Почтовый адрес',
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Фамилия пользователя',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография пользователя',
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Текущая роль пользователя',
    )
    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=15,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    constraints = [
        models.UniqueConstraint(
            fields=['username', 'email'], name='unique_user')
    ]

    def __str__(self):
        """Строковое представление модели."""
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
