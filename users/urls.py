from django.urls import path
from .views import signup, user_login, user_logout
from .views import (
    signup,
    user_login,
    user_logout,
    doctor_dashboard,
    patient_dashboard
)
from .views import book_slot

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("doctor/", doctor_dashboard),
    path("patient/", patient_dashboard),
    path("book/<int:slot_id>/", book_slot, name="book_slot"),
]