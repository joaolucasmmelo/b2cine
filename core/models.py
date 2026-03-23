from django.db import models

# # Create your models here.


class Movie(models.Model):
    name: str = models.CharField(max_length=128)
    description: str = models.TextField()
    duration_minutes: int = models.IntegerField()


class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(default=16)

    def __str__(self):
        return f"{self.id}"


class Session(models.Model):
    movie: Movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    room: Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Sessão para o filme: {self.movie.name}, na {self.room.name} as {self.datetime}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            [Seat.objects.create(session=self, seat_number=f"{row}{num}") for row in ['A', 'B', 'C', 'D'] for num in range(1, 5)]


class Seat(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    is_purchased = models.BooleanField(default=False)
