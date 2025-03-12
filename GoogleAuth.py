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