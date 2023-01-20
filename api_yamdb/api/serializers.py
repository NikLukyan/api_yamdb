from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Title


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
