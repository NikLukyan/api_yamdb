from django.db.models import Avg
from rest_framework import serializers

from api.validators import UserDataValidation
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:

        model = Genre
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = Title

    def get_rating(self, obj):
        return (Review.objects.filter(title=obj).
                aggregate(Avg('score')).
                get("score__avg"))


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    # title = serializers.SlugRelatedField(queryset=Title.objects.all(),
    #                                      slug_field='name')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        # validators = (UniqueTogetherValidator(
        #     queryset=Reviews.objects.all(),
        #     fields=('author', 'title'),
        #     message='Вы уже написали отзв на это произведение.'
        #     ),
        # )

        # read_only_fields = ("title",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment



class SignUpSerializer(serializers.ModelSerializer,  UserDataValidation):
    """Сериализатор для создания пользователя"""
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)

    class Meta:
        fields = ('email', 'username')
        model = User


class UserSerializer(serializers.ModelSerializer, UserDataValidation):
    """Сериализатор модели User"""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

class JWTTokenAPIViewSerializer(serializers.ModelSerializer, UserDataValidation):
    "Сериализатор данных для получения JWT токена"
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


class ProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)
