from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")

client = TelegramClient('session_name', api_id, api_hash)

session_name = 'my_session'

if not api_id or not api_hash or not channel_username:
    raise ValueError("Missing API credentials. Check your .env file.")

# Initialize Telegram client
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    # Iterate through the first 100 messages in the channel
    async for message in client.iter_messages(channel_username, limit=100):
        # Check if the message has text or is an image
        if message.text:
            print(f"Text Message: {message.text}")
        elif message.photo:
            print(f"Image Message: {message.id} (Image detected, not text)")
        else:
            print("[No Text or Image Found]")

        print('-' * 50)  # Separator between each message for clarity

with client:
    client.loop.run_until_complete(main())