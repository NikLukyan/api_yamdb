from django.contrib import admin

from .models import Reviews, Category, Comment, Title, Genre
from users.models import User


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'username',
#         'email',
#         'first_name',
#         'last_name',
#         'role',
#     )
#
#
# admin.site.register(User, UserAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Genre)
