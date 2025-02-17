from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from .env
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")
telegram_id = int(os.getenv("TELEGRAM_ID"))
# telegram_username = 

# Check if API credentials or channel username is missing
if not api_id or not api_hash or not channel_username or not telegram_id:
    raise ValueError("Missing API credentials or channel username. Check your .env file.")

# Initialize Telegram client
session_name = 'my_session'
client = TelegramClient('session_name', api_id, api_hash)


async def main():
    async for message in client.iter_messages(channel_username, limit=10):
        if message.text or message.photo:
            print(f"Forwarding message ID: {message.id}")
            await client.forward_messages(telegram_id, message.id, channel_username)
        else:
            print("[No Text or Image Found]")

        print('-' * 50)  # Separator between each message for clarity

# Run the client and execute the main function
with client:
    client.loop.run_until_complete(main())