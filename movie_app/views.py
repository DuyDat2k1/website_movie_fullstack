from django.views.generic import ListView
from django.db.models import Q
from .models import Movie

class MovieListView(ListView):
    model = Movie
    template_name = 'movie_app/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q))
        return qs
