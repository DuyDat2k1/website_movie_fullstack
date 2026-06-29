from django.contrib import admin
from .models import Movie, Genre, Country


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_type', 'country', 'release_year', 'is_featured', 'views', 'display_genres']
    list_filter = ['movie_type', 'country', 'release_year', 'is_featured']
    search_fields = ['title', 'title_original']
    filter_horizontal = ['genres']
    readonly_fields = ['views']

    def display_genres(self, obj):
        return ", ".join(genre.name for genre in obj.genres.all()[:3])
    display_genres.short_description = "Thể loại"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
