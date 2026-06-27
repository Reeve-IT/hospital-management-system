from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from appointments.models import Availability
from django.utils import timezone
from django.shortcuts import get_object_or_404
from appointments.services import create_booking
from appointments.forms import AvailabilityForm
from appointments.email_service import send_signup_email

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_signup_email(user.email)
            return redirect("/signup/")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            if user.role == "DOCTOR":
                return redirect("/doctor/")

            return redirect("/patient/")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("/login/")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            if user.role == "DOCTOR":
                return redirect("/doctor/")

            return redirect("/patient/")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("/login/")


@login_required
def doctor_dashboard(request):

    if request.user.role != "DOCTOR":
        return redirect("/patient/")

    if request.method == "POST":
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()

            return redirect("/doctor/")

    else:
        form = AvailabilityForm()

    slots = Availability.objects.filter(
        doctor=request.user
    ).order_by(
        "date",
        "start_time"
    )

    return render(
        request,
        "doctor.html",
        {
            "form": form,
            "slots": slots
        }
    )

@login_required
def patient_dashboard(request):

    slots = Availability.objects.filter(
        is_booked=False,
        date__gte=timezone.now().date()
    ).order_by(
        "date",
        "start_time"
    )

    return render(
        request,
        "patient.html",
        {
            "slots": slots
        }
    )

@login_required
def book_slot(request, slot_id):

    slot = get_object_or_404(Availability, id=slot_id)

    try:
        create_booking(request.user, slot.id)
    except Exception:
        return redirect("/patient/")

    return redirect("/patient/")