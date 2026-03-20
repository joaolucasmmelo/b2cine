from rest_framework import generics
from .models import Movie, Session, Seat
from .serializers import MovieSerializer, SessionSerializer, SeatMapSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SessionsPerMovieListView(generics.ListAPIView):
    serializer_class = SessionSerializer

    def get_queryset(self):
        return Session.objects.filter(movie_id=self.kwargs['movie_id'])


class SessionSeatListView(generics.ListAPIView):
    serializer_class = SeatMapSerializer
    pagination_class = None

    def get_queryset(self):
        return Seat.objects.filter(session_id=self.kwargs['session_id']).order_by('seat_number')
