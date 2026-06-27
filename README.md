# Mini Hospital Management System (HMS)

## Setup and Run

### Prerequisites

* Python 3.12+
* Git
* Google Calendar API Credentials (`credentials.json`)
* Gmail App Password (for email notifications)

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd hospital-management-system
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Google Calendar

1. Create a Google Cloud project.
2. Enable the Google Calendar API.
3. Create OAuth Desktop Application credentials.
4. Download the credentials file.
5. Rename it to:

```
credentials.json
```

6. Place it in the project root directory.

The first time an appointment is booked, Google OAuth will open in the browser and create a `token.pickle` file after successful authentication.

### Start the Email Service

Navigate to the `email-service` folder.

```bash
cd email-service
python app.py
```

The email service will start on:

```
http://127.0.0.1:5000
```

### Start the Django Application

Return to the project root.

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000
```

---

## System Architecture

The application is divided into two independent components.

### Django Backend

Responsible for:

* User Authentication
* Role-based Authorization
* Doctor Dashboard
* Patient Dashboard
* Availability Management
* Appointment Booking
* Booking Validation
* Google Calendar Integration

### Email Service

A separate local HTTP service built using Flask.

Responsibilities:

* SIGNUP_WELCOME email notification
* BOOKING_CONFIRMATION email notification

The Django backend communicates with the email service using HTTP requests.

### Database

The system stores:

* Users
* Doctor Availability
* Patient Bookings

The relationship is:

```
Doctor
   │
   ├── Availability Slots
   │
Patient
   │
   └── Booking
```

Each booking references exactly one availability slot.

### Role-Based Access

Doctor:

* Create availability
* View only their own availability
* View booking status of their slots

Patient:

* View available slots
* Book available appointments

Patients cannot access doctor functionality and doctors cannot access patient-only functionality.

### Google Calendar Integration

When an appointment is booked:

* A Google Calendar event is created.
* Event title contains the doctor's name.
* Event time matches the selected appointment slot.

### Email Notifications

Two email notifications are supported:

* Welcome Email after successful registration
* Booking Confirmation after successful appointment booking

---

## The Design Decision

### Problem

Prevent two patients from booking the same appointment slot at the same time.

### Option 1

Check if the slot is available before creating a booking.

This approach is unsafe because two users could read the same slot simultaneously and both create bookings.

### Option 2 (Chosen)

Use a database transaction with row locking.

The booking logic uses:

* `transaction.atomic()`
* `select_for_update()`

This locks the selected availability record while the booking is being created.

### Why This Was Chosen

Using database transactions guarantees that only one booking can be created for a slot, even if multiple users attempt to book it simultaneously.

This approach is more reliable and prevents race conditions.

---

## Limitations

This project is a prototype intended for local development.

Current limitations include:

* Email service runs locally and is not deployed to a cloud provider.
* Google Calendar currently authenticates a single Google account for demonstration purposes.
* Doctor availability can be created but advanced editing and deletion features are limited.
* Basic HTML templates are used instead of a production-ready frontend.
* Error handling and input validation can be improved.
* Additional security features such as rate limiting and audit logging are not implemented.

---

## Features

* Doctor Registration
* Patient Registration
* Login & Logout
* Role-Based Authentication
* Doctor Dashboard
* Patient Dashboard
* Create Availability Slots
* View Available Slots
* Book Appointment
* Automatic Slot Blocking
* Race Condition Protection
* Google Calendar Integration
* Welcome Email Notification
* Booking Confirmation Email

---

## Technologies Used

* Python
* Django
* Django ORM
* SQLite
* Flask
* Google Calendar API
* Gmail SMTP (Yagmail)
* HTML
* CSS
* Git
* GitHub
