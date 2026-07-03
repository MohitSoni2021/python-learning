import base64
import os
import pickle

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_emails():
    service = get_gmail_service()

    results = service.users().messages().list(userId="me", maxResults=10).execute()

    messages = results.get("messages", [])

    for i, msg in enumerate(messages):
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()

        headers = msg_data["payload"]["headers"]

        subject = ""
        sender = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]
            if header["name"] == "From":
                sender = header["value"]

        print(f"\nEmail {i + 1}")
        print("From:", sender)
        print("Subject:", subject)


if __name__ == "__main__":
    fetch_emails()
