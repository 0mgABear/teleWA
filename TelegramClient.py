from telethon import TelegramClient
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

# Retrieve Telegramm API credentials from .env
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")
telegram_username = os.getenv("TELEGRAM_USERNAME")  # This can be @username or numeric user ID

# Retrieve Twilio Credentials
account_sid = os.getenv("TWILIO_LIVE_SID")
auth_token = os.getenv("TWILIO_LIVE_AUTH_TOKEN")
twilio_WA_number = os.getenv("TWILIO_WA_NUMBER")
recipient_WA_number = os.getenv("RECIPIENT_WA_NUMBER")

# Check if API credentials or channel username is missing
if not api_id or not api_hash or not channel_username or not account_sid or not auth_token:
    raise ValueError("Missing API credentials or channel username. Check your .env file.")

# Initialize Telegram client & Twilio Client
session_name = 'my_session'
client = TelegramClient(session_name, api_id, api_hash)
twilio_client = Client(account_sid, auth_token)

async def main():
    async for message in client.iter_messages(channel_username, limit=5):
        if message.text:
            print(f"Forwarding message ID: {message.id}")

            # Send Telegram message to WhatsApp
            twilio_client.messages.create(
                from_=twilio_WA_number,
                to=recipient_WA_number,
                body=message.text
            )

        print('-' * 50)

# Run the client and execute the main function
with client:
    client.loop.run_until_complete(main())