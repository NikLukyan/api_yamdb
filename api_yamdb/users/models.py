from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        ('USER', 'user'),
        ('MODERATOR','moderator'),
        ('ADMIN', 'admin'),
    ]
    username = models.CharField(
        max_length=150,
        db_index=True,
        unique=True,
        verbose_name='Логин',
    )
    email = models.EmailField(
        max_length=254,
        db_index=True,
        unique=True,
        verbose_name='Эл. адрес',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=10,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff
    
    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
    
    @property
    def is_user(self):
        return self.role == self.USER


    
    


    

    pass

