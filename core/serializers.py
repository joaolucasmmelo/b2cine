from .models import Movie, Session, Seat
from rest_framework import serializers
from django.core.cache import cache


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'duration_minutes']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'movie', 'room', 'datetime']


class SeatMapSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'status']

    def get_status(self, obj):
        if obj.is_purchased:
            return 'Purchased'

        if cache.get(f"seat_lock_{obj.session_id}_{obj.seat_number}"):
            return 'Reserved'

        return 'Available'
