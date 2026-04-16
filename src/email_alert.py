import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

EMAIL_RECEIVER = "receiver_email@gmail.com"

def send_email_alert(error_count):

    subject = "🚨 Devops Log Monitoring Alert"

    body = f"""
Alert!

Error detected in system logs.bool

Total Errors: {error_count}

Please check the monitoring report.
"""
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        print("Email alert sent!")

    except Exception as e:
        
        print("Email alert failed:", e)