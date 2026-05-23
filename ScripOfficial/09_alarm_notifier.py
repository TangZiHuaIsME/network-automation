import smtplib
import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from netmiko import ConnectHandler

DEVICES = [
    {
        "name": "Core-Router-01",
        "device_type": "cisco_ios",
        "host": "10.10.20.48",
        "username": "admin",
        "password": "C1sco12345",
    },
]

# Store credentials in environment variables — never hardcode in GitHub
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = os.environ.get("EMAIL_FROM", "your@gmail.com")
EMAIL_TO   = os.environ.get("EMAIL_TO",   "your@gmail.com")
EMAIL_PASS = os.environ.get("EMAIL_PASS",  "your-app-password")

def send_alert(device_name: str, device_ip: str, error: str):
    subject = f"[ALERT] Device Down: {device_name} ({device_ip})"
    body = (
        f"Device: {device_name}\n"
        f"IP: {device_ip}\n"
        f"Time: {datetime.datetime.now()}\n"
        f"Error: {error}\n\n"
        f"Please investigate immediately."
    )
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"  Email alert sent for {device_name}")
    except Exception as e:
        print(f"  Failed to send email: {e}")

def check_device(device: dict) -> bool:
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        connection.disconnect()
        return True
    except Exception as e:
        send_alert(device["name"], device["host"], str(e))
        return False

def main():
    print(f"\n Alarm Notifier — {datetime.datetime.now()}\n")
    for device in DEVICES:
        reachable = check_device(device)
        icon = "✓" if reachable else "✗"
        status = "reachable" if reachable else "UNREACHABLE — alert sent"
        print(f"  {icon} {device['name']} — {status}")

if __name__ == "__main__":
    main()
