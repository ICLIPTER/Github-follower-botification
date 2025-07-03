import requests
import json
import os
from dotenv import load_dotenv
from send_email import send_email_notification

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FOLLOWERS_FILE = "followers.json"

def get_followers(username, token=None):
    url = f"https://api.github.com/users/{username}/followers"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return [user["login"] for user in response.json()]

def load_previous_followers():
    if os.path.exists(FOLLOWERS_FILE):
        with open(FOLLOWERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_followers(followers):
    with open(FOLLOWERS_FILE, "w") as f:
        json.dump(followers, f)

def main():
    current = get_followers(GITHUB_USERNAME, GITHUB_TOKEN)
    previous = load_previous_followers()
    new_followers = list(set(current) - set(previous))

    if new_followers:
        print(f"🆕 New followers: {new_followers}")
        send_email_notification(new_followers)
        save_followers(current)
    else:
        print("✅ No new followers.")

if __name__ == "__main__":
    main()
