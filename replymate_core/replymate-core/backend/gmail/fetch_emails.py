
from googleapiclient.discovery import build

def get_latest_thread(creds, max_messages: int = 5) -> str:
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(
        userId='me', maxResults=max_messages, labelIds=['INBOX']
    ).execute()
    messages = results.get('messages', [])

    snippets = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject','From']
        ).execute()
        snippet = msg_data.get('snippet', '')
        snippets.append(f"From: {msg_data['payload']['headers'][1]['value']}\nSubject: {msg_data['payload']['headers'][0]['value']}\n{snippet}")

    return "\n---\n".join(snippets)
