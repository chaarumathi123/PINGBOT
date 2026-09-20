"""
Step 2: AI-powered SMS/WhatsApp bot using Twilio + Groq.

WHAT CHANGED FROM STEP 1:
- We no longer just reverse the text. Instead we send it to an LLM
  (via Groq's API) and reply with whatever the AI says back.
- We load the Groq API key from a .env file instead of hardcoding it,
  so the real key never ends up in your code or on GitHub.
"""

import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from groq import Groq

# load_dotenv() reads your .env file and makes its contents available
# via os.environ / os.getenv(), as if you'd set them in your terminal.
load_dotenv()

# os.getenv("GROQ_API_KEY") reads the value of GROQ_API_KEY from your
# .env file. If it's missing, this returns None instead of crashing
# immediately — we'll find out fast anyway the first time we call Groq.
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)


def ask_ai(user_message):
    """
    Sends the user's message to Groq's LLM and returns the AI's reply
    as a plain string. Kept as its own function so app.py stays
    readable — sms_reply() below just calls this and doesn't need to
    know HOW the AI call works.
    """
    # chat.completions.create() is the standard shape used by most
    # LLM APIs (Groq copies OpenAI's format on purpose, so this same
    # code pattern would work with OpenAI too with small changes).
    response = client.chat.completions.create(
        # This picks WHICH model on Groq's servers answers the request.
            model="openai/gpt-oss-120b",
        messages=[
            # "system" sets the AI's behavior/personality for the whole
            # conversation. We keep replies short since this is SMS/WhatsApp,
            # not a chat app with unlimited scroll space.
            {
                "role": "system",
                "content": "You are a helpful assistant replying over SMS. "
                            "Keep answers short (under 3 sentences) and clear."
            },
            # "user" is the actual message the person sent.
            {"role": "user", "content": user_message},
        ],
    )

    # The API returns a structured object. This line digs into it to
    # pull out just the text of the AI's reply.
    return response.choices[0].message.content


@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.values.get("Body", "")

    resp = MessagingResponse()

    # If someone texts nothing (shouldn't normally happen, but good practice),
    # don't call the AI with an empty string.
    if incoming_msg.strip():
        ai_reply = ask_ai(incoming_msg)
    else:
        ai_reply = "Send me a question and I'll do my best to answer!"

    resp.message(ai_reply)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
