import requests
import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIGURATION ===
GITHUB_USERNAME = "YOUR_GITHUB_USERNAME"
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"  # optional for higher rate limit
EMAIL_SENDER = "your_email@example.com"
EMAIL_RECEIVER = "receiver_email@example.com"
EMAIL_PASSWORD = "your_email_password"  # App password if using Gmail
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587
FOLLOWERS_FILE = "followers.json"
# =====================

def get_followers(username, token=None):
    url = f"https://api.github.com/users/{username}/followers"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return [user["login"] for user in response.json()]

def send_email_notification(new_followers):
    subject = "🚨 New GitHub Follower(s)"
    body = f"New follower(s) detected:\n\n" + "\n".join(new_followers)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    print("📧 Email sent!")

def load_previous_followers():
    if os.path.exists(FOLLOWERS_FILE):
        with open(FOLLOWERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_followers(followers):
    with open(FOLLOWERS_FILE, "w") as f:
        json.dump(followers, f)

def main():
    current_followers = get_followers(GITHUB_USERNAME, GITHUB_TOKEN)
    previous_followers = load_previous_followers()
    new_followers = list(set(current_followers) - set(previous_followers))

    if new_followers:
        print(f"🆕 New followers: {new_followers}")
        send_email_notification(new_followers)
        save_followers(current_followers)
    else:
        print("✅ No new followers.")

if __name__ == "__main__":
    main()
