from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Title, Reviews, Comment


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
        return int(Reviews.objects.filter(title=obj).
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
