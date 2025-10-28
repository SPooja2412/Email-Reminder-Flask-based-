from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import threading

app = Flask(__name__)

# Function to send email
def send_email(sender_email, receiver_email, app_password, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(message)
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error:", e)

# Run schedule in background
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(30)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sender_email = request.form["sender"]
        app_password = request.form["password"]
        receiver_email = request.form["receiver"]
        subject = request.form["subject"]
        body = request.form["body"]
        time_input = request.form["time"]

        schedule.clear()
        schedule.every().day.at(time_input).do(
            send_email, sender_email, receiver_email, app_password, subject, body
        )

        return render_template(
            "success.html",
            sender=sender_email,
            receiver=receiver_email,
            subject=subject,
            body=body,
            time_input=time_input,
        )

    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=run_schedule).start()
    app.run(debug=True)
