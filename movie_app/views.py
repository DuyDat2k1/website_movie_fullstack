from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Movie, Genre, Country, Episode


class MovieListView(ListView):
    model = Movie
    template_name = 'movie_app/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 24

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(title_original__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_movies'] = Movie.objects.filter(is_featured=True)[:8]
        context['series_movies'] = Movie.objects.filter(movie_type='series')[:12]
        context['cinema_movies'] = Movie.objects.filter(movie_type='cinema')[:12]
        context['latest_movies'] = Movie.objects.filter(movie_type='single')[:12]
        context['animation_movies'] = Movie.objects.filter(movie_type='animation')[:12]
        context['trending_movies'] = Movie.objects.order_by('-views')[:12]
        context['genres'] = Genre.objects.all()
        context['countries'] = Country.objects.all()
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_app/movie_detail.html'
    context_object_name = 'movie'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        episodes = movie.episodes.all()
        context['episodes'] = episodes
        context['server_names'] = list(set(episodes.values_list('server_name', flat=True)))
        context['genres'] = Genre.objects.all()
        context['countries'] = Country.objects.all()
        context['related_movies'] = Movie.objects.filter(
            genres__in=movie.genres.all()
        ).exclude(id=movie.id).distinct()[:8]

        first = episodes.first()
        context['current_episode'] = first
        return context


def episode_detail(request, episode_id):
    episode = get_object_or_404(Episode, id=episode_id)
    return JsonResponse({
        'id': episode.id,
        'name': episode.name,
        'link_embed': episode.link_embed,
        'link_m3u8': episode.link_m3u8,
        'server_name': episode.server_name,
    })
