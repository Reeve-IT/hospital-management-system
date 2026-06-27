from django.db import models
from users.models import User


class Availability(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.username} - {self.date} {self.start_time}"


class Booking(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_bookings"
    )

    slot = models.OneToOneField(
        Availability,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slot.is_booked = True
        self.slot.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username} booked {self.doctor.username}"