from django.contrib import admin
from .models import Movie, Genre

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'display_genres', 'created_at']
    search_fields = ['title']
    filter_horizontal = ['genres']

    def display_genres(self, obj):
        return ", ".join(genre.name for genre in obj.genres.all())
    display_genres.short_description = "Thể loại"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
