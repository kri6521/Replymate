
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build

def send_email(creds, to: str, subject: str, body: str):
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return service.users().messages().send(
        userId='me', body={'raw': raw}
    ).execute()
