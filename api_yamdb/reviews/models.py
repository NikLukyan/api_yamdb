from django.db import models
# from api_yamdb.api.models import Title


class Reviews(models.Model):
    author = models.IntegerField('Номер пользователя')
    # models.ForeignKey(
    # User, on_delete=models.CASCADE, related_name='reviews')

    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField('Рейтинг', )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
