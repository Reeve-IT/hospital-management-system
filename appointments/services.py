from django.db import transaction
from .models import Availability, Booking
from .google_calendar import create_event
from datetime import datetime
from .email_service import send_booking_email

def create_booking(patient, slot_id):
    with transaction.atomic():

        slot = Availability.objects.select_for_update().get(
            id=slot_id
        )

        if slot.is_booked:
            raise Exception("Slot already booked")

        booking = Booking.objects.create(
            patient=patient,
            doctor=slot.doctor,
            slot=slot
        )

        slot.is_booked = True
        slot.save()
        
        start = datetime.combine(slot.date, slot.start_time)
        end = datetime.combine(slot.date, slot.end_time)

        create_event(
           f"Appointment with Dr. {slot.doctor.username}",
           start,
           end
           )
        send_booking_email(patient.email)
        return booking