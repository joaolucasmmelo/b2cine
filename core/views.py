from rest_framework import generics
from .models import Movie, Session, Seat
from .serializers import MovieSerializer, SessionSerializer, SeatMapSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class MovieListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SessionsPerMovieListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer

    def get_queryset(self):
        return Session.objects.filter(movie_id=self.kwargs['movie_id'])


class SessionSeatListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SeatMapSerializer
    pagination_class = None

    def get_queryset(self):
        return Seat.objects.filter(session_id=self.kwargs['session_id']).order_by('seat_number')


class ReserveSeatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id, seat_number):
        seat = get_object_or_404(Seat, session_id=session_id, seat_number=seat_number)
        lock_key = f"seat_lock_{seat.session_id}_{seat.seat_number}_{request.user.id}"
        if seat.is_purchased:
            return Response({'error': 'Seat already purchased'}, status=400)
        try:
            result = cache.incr(lock_key)
        except ValueError:
            cache.set(lock_key, 1, timeout=600)
            result = 1
        if result > 1:
            return Response({'error': 'Seat is currently reserved'}, status=400)

        return Response({'message': 'Seat sucessfully reserved for 10 minutes'})


class BuySeatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, session_id, seat_number):

        lock_key = f"seat_lock_{session_id}_{seat_number}_{request.user.id}"
        exist = cache.get(lock_key)

        if not exist:
            return Response({'error': 'Seat is not reserved'}, status=400)
        seat = get_object_or_404(Seat, session_id=session_id, seat_number=seat_number)
        if seat.is_purchased:
            return Response({'error': 'Seat already purchased'}, status=400)

        seat.is_purchased = True
        seat.save()
        cache.delete(lock_key)
        return Response({'message': 'Seat purchased successfully'})
