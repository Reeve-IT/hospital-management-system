import requests

URL = "http://127.0.0.1:5000/send-email"

def send_signup_email(email):
    print("Sending welcome email to:", email)

    response = requests.post(
        URL,
        json={
            "trigger": "SIGNUP_WELCOME",
            "email": email
        }
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

def send_booking_email(email):
    requests.post(
        URL,
        json={
            "trigger": "BOOKING_CONFIRMATION",
            "email": email
        }
    )