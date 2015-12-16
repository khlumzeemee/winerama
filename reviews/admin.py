from django.contrib import admin
from .models import Wine, Review


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('wine', 'rating',  'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']


class WineAdmin(admin.ModelAdmin):
    model = Wine
    search_fields = ['name']
    list_filter = ['name']

admin.site.register(Wine, WineAdmin)
admin.site.register(Review, ReviewAdmin)