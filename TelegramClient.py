from telethon import TelegramClient
import os
from dotenv import load_dotenv
from twilio.rest import Client
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Load environment variables from .env file
load_dotenv()

# Retrieve Telegram API credentials from .env
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_username = os.getenv("CHANNEL_USERNAME")
telegram_username = os.getenv("TELEGRAM_USERNAME")

# Retrieve Twilio Credentials
account_sid = os.getenv("TWILIO_LIVE_SID")
auth_token = os.getenv("TWILIO_LIVE_AUTH_TOKEN")
twilio_WA_number = os.getenv("TWILIO_WA_NUMBER")
recipient_WA_number = os.getenv("RECIPIENT_WA_NUMBER")

# Google Drive authentication
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
gauth.Authorize()
drive = GoogleDrive(gauth)

# Check if API credentials or channel username is missing
if not api_id or not api_hash or not channel_username or not account_sid or not auth_token:
    raise ValueError("Missing API credentials or channel username.")

# Initialize Telegram client & Twilio Client
session_name = 'my_session'
client = TelegramClient(session_name, api_id, api_hash)
twilio_client = Client(account_sid, auth_token)

async def main():
    # Iterate through the last 5 messages in the channel
    async for message in client.iter_messages(channel_username, limit=5):
        if message.text:
            # Send Telegram message to WhatsApp
            twilio_client.messages.create(
                from_=twilio_WA_number,
                to=recipient_WA_number,
                body=message.text  # Forward the text of the message
            )

        elif message.media:
            print(f"Message ID: {message.id} contains media. Downloading and uploading to Google Drive...")

            # Download the media to a temporary location
            file_path = f"temp_media_{message.id}.jpg"  # You can customize the file name based on the message ID or type
            await message.download_media(file_path)
            gdrive_file = drive.CreateFile({'title': f'media_{message.id}.jpg'})  # Change the title accordingly
            gdrive_file.SetContentFile(file_path)
            gdrive_file.Upload()
            gdrive_file.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'
            })

            # Print the Google Drive file ID (optional)
            print(f"Uploaded media file to Google Drive with ID: {gdrive_file['id']}")

            # Delete the local temporary file
            os.remove(file_path)

            # Send the media file via Twilio WhatsApp
            file_url = f"https://drive.google.com/uc?id={gdrive_file['id']}"
            print(f"Public URL for file: {file_url}")

            # Send the media file via Twilio WhatsApp
            twilio_client.messages.create(
                from_=twilio_WA_number,
                to=recipient_WA_number,
                body=message.text,
                media_url=[file_url]  # Send the media file URL to WhatsApp
            )

            # Optional: Delete the file from Google Drive after sending to WhatsApp
            gdrive_file.Delete()
            print(f"Deleted file from Google Drive with ID: {gdrive_file['id']}")

        print('-' * 50)  # Separator for clarity

# Run the client and execute the main function
with client:
    client.loop.run_until_complete(main())