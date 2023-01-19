from django.contrib import admin

from .models import Reviews


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Reviews, ReviewsAdmin)
