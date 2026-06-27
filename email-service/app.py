from flask import Flask, request, jsonify
import yagmail

app = Flask(__name__)

EMAIL = "dabreoreeve89@gmail.com"
PASSWORD = "xjppcczkvkmidgyk"

def send_email(to, subject, body):
    yag = yagmail.SMTP(EMAIL, PASSWORD)
    yag.send(to=to, subject=subject, contents=body)

@app.route("/send-email", methods=["POST"])
def email():

    data = request.json

    trigger = data["trigger"]
    receiver = data["email"]

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

    return jsonify({"message": "Email Sent"})

if __name__ == "__main__":
    app.run(port=5000)