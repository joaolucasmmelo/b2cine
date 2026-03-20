from django.urls import path
from .views import MovieListView, SessionsPerMovieListView, SessionSeatListView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/sessions/', SessionsPerMovieListView.as_view(), name='movie-sessions'),
    path('sessions/<int:session_id>/seats/', SessionSeatListView.as_view(), name='session-seats'),
]
