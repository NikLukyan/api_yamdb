from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Reviews, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        # fields = '__all__'
        model = Genre
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        # fields = '__all__'
        model = Category
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        fields = '__all__'
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
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    # title = serializers.SlugRelatedField(queryset=Title.objects.all(),
    #                                      slug_field='name')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews
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




# class FollowSerializer(serializers.ModelSerializer):
#     user = SlugRelatedField(
#         read_only=True, slug_field='username',
#         default=serializers.CurrentUserDefault()
#     )
#     following = SlugRelatedField(
#         queryset=User.objects.all(),
#         slug_field='username'
#     )
#
#     class Meta:
#         model = Follow
#         fields = ('user', 'following')
#         validators = (
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following'),
#                 message='Вы уже подписаны на этого автора.'
#             ),
#         )
#
#     def validate_following(self, value):
#         if self.context['request'].user == value:
#             raise serializers.ValidationError(
#                 'Нельзя подписаться на себя.')
#         return value



class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""
    class Meta:
        fields = ('email', 'username')
        model = User
    
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено!'
            )

        email = value.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Пользователь с email \'{email}\' уже существует.'
            )
        
        username = value.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь \'{username}\' уже существует.'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
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
    def validate_role(self, role):
        req_user = self.context['request'].user
        user = User.objects.get(username=req_user)
        if user.is_user:
            role = user.role
        return role


class JWTTokenAPIViewSerializer(serializers.ModelSerializer):
    "Сериализатор данных для получения JWT токена"
    username_field = User.email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        password = self.context['request'].data.get('confirmation_code')
        attrs['password'] = password
        return super().validate(attrs)
