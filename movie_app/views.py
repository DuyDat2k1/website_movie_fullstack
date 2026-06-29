from django.views.generic import ListView
from django.db.models import Q
from .models import Movie, Genre, Country


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
