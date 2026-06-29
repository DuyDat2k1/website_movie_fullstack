from django.contrib import admin
from .models import Movie, Genre, Country, Episode


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0
    fields = ['server_name', 'name', 'episode_number', 'link_embed', 'link_m3u8']
    ordering = ['sort_order', 'episode_number']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_type', 'country', 'release_year', 'is_featured', 'views', 'display_genres']
    list_filter = ['movie_type', 'country', 'release_year', 'is_featured']
    search_fields = ['title', 'title_original', 'slug']
    filter_horizontal = ['genres']
    readonly_fields = ['views']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EpisodeInline]

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


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'server_name', 'name', 'episode_number']
    list_filter = ['movie', 'server_name']
    search_fields = ['movie__title']
