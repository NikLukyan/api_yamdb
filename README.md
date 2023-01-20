# API_FINAL_YATUBE
## Описание

Это социальная сеть, которая даст пользователям возможность создать учетную запись, публиковать записи, подписываться на любимых авторов и отмечать понравившиеся записи.

## Установка

- Клонировать репозиторий и перейти в него в командной строке
- Cоздать и активировать виртуальное окружение:
    -python -m venv env
    -source env/bin/activate
    -python -m pip install --upgrade pip
- Установить зависимости из файла requirements.txt:
    -pip install -r requirements.txt
- Выполнить миграции:
   -python manage.py migrate
- Запустить проект:
    -python manage.py runserver

## Примеры 
from django.urls import include, path  
from rest_framework.routers import DefaultRouter  
from .views import (
    GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet
)

router = DefaultRouter()  
router.register('posts', PostViewSet, basename='posts')  
router.register('groups', GroupViewSet, basename='posts')  
router.register('follow', FollowViewSet, basename='followers')  
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
    basename='comments'
)  
urlpatterns = [  
    path('v1/', include(router.urls)),  
    path('v1/', include('djoser.urls')),  
    path('v1/', include('djoser.urls.jwt')),  
]
