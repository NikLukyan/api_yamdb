from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.v1.validators import UserDataValidation
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    confirmation_code = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


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

    def validate(self, data):
        """Валидируем, что пользователь не будет использовать
           никнейм, конфликтующий с эндпоинтом.
        """
        if data.get('username') != 'me':
            return data
        raise serializers.ValidationError(
            'Невозможное имя пользователя'
        )


class SignUpSerializer(serializers.Serializer, UserDataValidation):
    """Сериализатор для создания пользователя"""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)


class JWTTokenAPIViewSerializer(serializers.Serializer, UserDataValidation):
    "Сериализатор данных для получения JWT токена"
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


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
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if (title.reviews.filter(author=author).exists()
                and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Недопустимое значение!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
