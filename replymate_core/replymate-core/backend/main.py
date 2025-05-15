import os
from fastapi import FastAPI
from pydantic import BaseModel
from auth.google_auth import get_credentials
from gmail.fetch_emails import get_latest_thread
from gmail.send_reply import send_email
from llm.gpt import generate_reply
from utils.logger import logger

app = FastAPI(title="ReplyMate")


class ReplyRequest(BaseModel):
    tone: str = "professional"
    to: str
    subject: str


@app.get("/")
async def root():
    return {"message": "ReplyMate backend is running!"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/reply")
async def auto_reply(req: ReplyRequest):
    creds = get_credentials()
    thread = get_latest_thread(creds)
    logger.info("Fetched email thread")

    draft = generate_reply(thread, tone=req.tone)
    logger.info("Generated draft reply")

    send_resp = send_email(creds, to=req.to, subject=req.subject, body=draft)
    logger.info(f"Sent email: {send_resp.get('id')}")

    return {"thread": thread, "draft": draft, "sentMessageId": send_resp.get("id")}
