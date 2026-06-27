from appointments.google_calendar import create_event
import datetime

start = datetime.datetime.now() + datetime.timedelta(minutes=5)
end = start + datetime.timedelta(minutes=30)

create_event(
    "Hospital Test Appointment",
    start,
    end
)

print("Done")