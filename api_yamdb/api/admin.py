# from django.contrib import admin
#
# from reviews.models import Api
#
# class ApiAdmin(admin.ModelAdmin):
#     list_display = ('id', 'text', 'author', 'score', 'pub_date',)
#     search_fields = ('text',)
#     list_filter = ('pub_date',)
#     empty_value_display = '-пусто-'
#
#
# admin.site.register(Reviews, ReviewsAdmin)
# from django.contrib import admin
#
# from users.models import User
#
#
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
#
#
# from django.contrib import admin
#
# from .models import Reviews
#
#
# class ReviewsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'text', 'author', 'score', 'pub_date',)
#     search_fields = ('text',)
#     list_filter = ('pub_date',)
#     empty_value_display = '-пусто-'
#
#
# admin.site.register(Reviews, ReviewsAdmin)
