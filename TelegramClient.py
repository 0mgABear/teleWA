from telethon import TelegramClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from .env
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")
telegram_username = os.getenv("TELEGRAM_USERNAME")  # This can be @username or numeric user ID

# Check if API credentials or channel username is missing
if not api_id or not api_hash or not channel_username or not telegram_username:
    raise ValueError("Missing API credentials or channel username. Check your .env file.")

# Initialize Telegram client
session_name = 'my_session'
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    async for message in client.iter_messages(channel_username, limit=5):
        if message.text or message.photo or message.media:
            # Forward the message as a forwarded message (not as a new message)
            if telegram_username.isdigit():
                user_id = int(telegram_username)  # Convert it to int if it's a user ID
                await client.forward_messages(user_id, message.id, channel_username)  # Forward as a real forwarded message
            else:
                # If telegram_username is a username (starts with '@')
                await client.forward_messages(telegram_username, message.id, channel_username)  # Forward as a real forwarded message
        else:
            print("[No Text, Photo, or Media Found]")

        print('-' * 50)  # Separator between each message for clarity

# Run the client and execute the main function
with client:
    client.loop.run_until_complete(main())