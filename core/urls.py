from django.urls import path
from .views import MovieListView, SessionsPerMovieListView, SessionSeatListView, ReserveSeatView, BuySeatView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/sessions/', SessionsPerMovieListView.as_view(), name='movie-sessions'),
    path('sessions/<int:session_id>/seats/', SessionSeatListView.as_view(), name='session-seats'),
    path('sessions/<int:session_id>/seats/<str:seat_number>/reserve/', ReserveSeatView.as_view(), name='seat-reserve'),
    path('sessions/<int:session_id>/seats/<str:seat_number>/buy/', BuySeatView.as_view(), name='seat-buy'),
]
