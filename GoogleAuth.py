# File to generate Google Authentication Credentials

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# Initialize Google Auth
gauth = GoogleAuth()

# Check if credentials are stored
if not os.path.exists("mycreds.txt"):  
    gauth.LocalWebserverAuth()  
else:
    gauth.LoadCredentialsFile("mycreds.txt")  # Load saved credentials

# Save credentials for the next run
gauth.SaveCredentialsFile("mycreds.txt") 

# Create GoogleDrive instance
drive = GoogleDrive(gauth)

# List all files from Google Drive
file_list = drive.ListFile({'q': "trashed=false"}).GetList()

# Print details of files in your Drive
if file_list:
    for file in file_list:
        print(f"File: {file['title']} - ID: {file['id']}")
else:
    print("No files found in your Google Drive.")