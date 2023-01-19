from django.db import models


# from api_yamdb.api.models import Title
# from api_yamdb.user.models import User





class Reviews(models.Model):
    SCORE_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                     (8, 8), (9, 9), (10, 10), ]
    author = models.IntegerField('Номер пользователя')
    # models.ForeignKey(
    # User, on_delete=models.CASCADE, related_name='reviews')

    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

