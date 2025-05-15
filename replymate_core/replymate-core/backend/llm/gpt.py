import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, OpenAIError

# Load environment variables from a .env at project root
load_dotenv()

# Initialize the v1 OpenAI client with your GPT-4 key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_reply(context: str, tone: str = "professional") -> str:
    """
    Sends the email thread context to GPT-4 and returns the draft reply.
    """
    prompt = (
        f"You are an AI assistant drafting an email reply in a {tone} tone.\n\n"
        f"Thread:\n{context}\n\n"
        "Reply:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
    except RateLimitError:
        raise RuntimeError("OpenAI rate limit exceeded; please try again later.")
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI API error: {e}")

    # Extract and return the assistant’s reply text
    return response.choices[0].message.content.strip()
