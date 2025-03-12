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
    added_grouped_ids = set()    
    async for message in client.iter_messages(channel_username, limit=10):
        media_urls = []  # Store media links
        temp_files = []  # Track local file paths for cleanup
        grouped_media = {}

        if message.text and not message.media:
            twilio_client.messages.create(
                from_=twilio_WA_number,
                to=recipient_WA_number,
                body=message.text
            )
        elif message.media:
            album_messages = []

            if message.grouped_id and message.grouped_id not in added_grouped_ids:
                added_grouped_ids.add(message.grouped_id)

                # Collect all media messages with the same grouped_id
                async for m in client.iter_messages(channel_username, limit=10):
                    if m.grouped_id == message.grouped_id:
                        album_messages.append(m)

                album_messages.sort(key=lambda m: m.date) 

                # Now process all media for that grouped_id
                for media_msg in album_messages:
                    file_path = f"temp_media_{media_msg.id}.jpg"
                    temp_files.append(file_path)
                    await media_msg.download_media(file_path)

                    gdrive_file = drive.CreateFile({'title': os.path.basename(file_path)})
                    gdrive_file.SetContentFile(file_path)
                    gdrive_file.Upload()
                    gdrive_file.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'
                    })

                    file_url = f"https://drive.google.com/uc?id={gdrive_file['id']}"
                    media_urls.append(file_url)

                    os.remove(file_path)

                for link in media_urls:
                    twilio_client.messages.create(
                        from_=twilio_WA_number,
                        to=recipient_WA_number,
                        body=message.text,
                        media_url=link
                    )

        print('-' * 50)  # Separator for clarity

# Run the client and execute the main function
with client:
    client.loop.run_until_complete(main())