# PingBot — AI-Powered WhatsApp Assistant

Text any question to a WhatsApp number and get an instant AI-generated answer back — built as a real two-way messaging integration using Twilio's Programmable Messaging API.

## How it works

```
Person sends WhatsApp message
        ↓
Twilio receives it, sends a webhook (HTTP POST) to this server
        ↓
Flask reads the message body
        ↓
Message is sent to an LLM (Groq API) for a response
        ↓
Response is wrapped in TwiML and returned to Twilio
        ↓
Twilio sends it back as a real WhatsApp reply
```

## Tech stack

- **Python + Flask** — lightweight webhook server
- **Twilio Programmable Messaging API** — receives and sends WhatsApp messages
- **Groq API** (Llama/GPT-OSS models) — generates the AI responses
- **python-dotenv** — keeps API keys out of source code

## Setup

1. Clone this repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your real Groq API key:
   ```
   GROQ_API_KEY=your_key_here
   ```
3. Run the server:
   ```
   python app.py
   ```
4. Expose it publicly (for local testing) with [ngrok](https://ngrok.com):
   ```
   ngrok http 5000
   ```
5. In the Twilio Console, set your WhatsApp Sandbox's "When a message comes in" webhook to:
   ```
   https://your-ngrok-url.ngrok-free.dev/sms
   ```

## What I learned building this

Setting up a real webhook integration end-to-end — handling incoming HTTP requests from a third-party API, generating dynamic responses with an LLM, and replying in the exact format (TwiML) the receiving service expects.

## Demo

*(screenshot of a real WhatsApp exchange goes here)*
