import os
import base64
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Configuration ---
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
DOWNLOAD_FOLDER = "attachments"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# --- Authentication ---
def gmail_authenticate():
    creds = None
    if os.path.exists("backend/client_secret_474704076992-iivttmanto6fdtie28u8l7e5m5u0cjkm.apps.googleusercontent.com.json"):
        creds = Credentials.from_authorized_user_file("backend/client_secret_474704076992-iivttmanto6fdtie28u8l7e5m5u0cjkm.apps.googleusercontent.com.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("backend/client_secret_474704076992-iivttmanto6fdtie28u8l7e5m5u0cjkm.apps.googleusercontent.com.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

# --- Download Attachments ---
def download_attachments(service, user_id='me', query="has:attachment"):
    results = service.users().messages().list(userId=user_id, q=query).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
        return

    for msg in messages:
        msg_id = msg["id"]
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        for part in message["payload"].get("parts", []):
            if part.get("filename"):
                filename = part["filename"]
                att_id = part["body"]["attachmentId"]
                attachment = service.users().messages().attachments().get(
                    userId=user_id, messageId=msg_id, id=att_id
                ).execute()
                data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
                filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"Downloaded: {filename}")

# --- Main ---
if __name__ == "__main__":
    service = gmail_authenticate()
    download_attachments(service)
