from django.db import models
from django.contrib.auth.models import User
from django.db import transaction


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Only set available_seats on creation (not on every update)
        if not self.pk or self.available_seats is None:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=1)  # ✅ Add this field
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number}"

    def save(self, *args, **kwargs):
        # Ensure atomic update of seats when creating or updating a booking
        with transaction.atomic():
            if not self.pk:
                # New booking: ensure enough seats
                if self.flight.available_seats is None:
                    self.flight.available_seats = self.flight.total_seats
                if self.seats_booked > self.flight.available_seats:
                    raise ValueError("Not enough seats available for this booking")
                # decrement available seats
                self.flight.available_seats -= self.seats_booked
                self.flight.save()
                super().save(*args, **kwargs)
            else:
                # Existing booking: adjust by delta
                old = Booking.objects.select_for_update().get(pk=self.pk)
                delta = self.seats_booked - old.seats_booked
                if delta > 0:
                    if self.flight.available_seats is None:
                        self.flight.available_seats = self.flight.total_seats
                    if delta > self.flight.available_seats:
                        raise ValueError("Not enough seats available to increase booking")
                    self.flight.available_seats -= delta
                elif delta < 0:
                    self.flight.available_seats -= delta  # subtracting negative -> add seats back
                self.flight.save()
                super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # When deleting a booking, return seats to flight
        with transaction.atomic():
            # refresh flight to avoid stale values
            f = Flight.objects.select_for_update().get(pk=self.flight.pk)
            if f.available_seats is None:
                f.available_seats = f.total_seats
            f.available_seats += self.seats_booked
            f.save()
            super().delete(*args, **kwargs)
