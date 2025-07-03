import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def send_email_notification(new_followers):
    sender = os.getenv("EMAIL_SENDER")
    receiver = os.getenv("EMAIL_RECEIVER")
    api_key = os.getenv("SENDGRID_API_KEY")

    if not all([sender, receiver, api_key]):
        print("❌ Missing one or more environment variables:")
        print(f"EMAIL_SENDER: {sender}")
        print(f"EMAIL_RECEIVER: {receiver}")
        print(f"SENDGRID_API_KEY: {'SET' if api_key else 'NOT SET'}")
        return

    subject = "🚨 New GitHub Follower(s)"
    content = "New follower(s):\n\n" + "\n".join(new_followers)

    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        plain_text_content=content,
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"📧 Email sent! Status: {response.status_code}")
        print(response.body)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
