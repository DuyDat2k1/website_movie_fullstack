from django.urls import path
from .views import MovieListView, MovieDetailView, episode_detail

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('api/movie/episode/<int:episode_id>/', episode_detail, name='episode_detail'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
]
