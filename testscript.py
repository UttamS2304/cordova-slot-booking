import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    connection.sendmail(
        from_addr=EMAIL_ADDRESS,
        to_addrs=["uttamsaxena2024@gmail.com"],  # <-- your actual email to test
        msg="Subject:Test Mail\n\nThis is a test email from Cordova app."
    )

print("✅ Test mail sent.")

