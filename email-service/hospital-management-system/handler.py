import json
import yagmail

EMAIL = "dabreoreeve89@gmail.com"
PASSWORD = "xjppcczkvkmidgyk"

def send_email(to, subject, body):
    yag = yagmail.SMTP(EMAIL, PASSWORD)
    yag.send(
        to=to,
        subject=subject,
        contents=body
    )

def hello(event, context):

    body = json.loads(event["body"])

    trigger = body["trigger"]
    receiver = body["email"]

    if trigger == "SIGNUP_WELCOME":

        send_email(
            receiver,
            "Welcome",
            "Welcome to Hospital Management System!"
        )

    elif trigger == "BOOKING_CONFIRMATION":

        send_email(
            receiver,
            "Booking Confirmed",
            "Your appointment has been booked successfully."
        )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Email Sent"})
    }