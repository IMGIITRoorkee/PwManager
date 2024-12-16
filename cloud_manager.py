import os
import json
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class CloudManager:
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    def __init__(self, credentials_path, token_path='token.pickle'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.files_record_path = "uploaded_files.json"
        self.authenticate()
        self.ensure_file_record_exists()

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('drive', 'v3', credentials=creds)

    def ensure_file_record_exists(self):
        if not os.path.exists(self.files_record_path):
            with open(self.files_record_path, 'w') as f:
                json.dump({}, f)

    def record_uploaded_files(self, name, file_id):
        with open(self.files_record_path, 'r+') as f:
            data = json.load(f)
            data[name] = file_id
            f.seek(0)
            json.dump(data, f, indent=4)

    def get_file_id(self, file_name):
        with open(self.files_record_path, 'r') as f:
            data = json.load(f)
            return data.get(file_name)

    def upload_file(self, file_path, file_name):
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        self.record_uploaded_files(file_name, file_id)
        return file_id

    def download_file(self, file_name, destination_path):
        file_id = self.get_file_id(file_name)
        if not file_id:
            raise FileNotFoundError(f"File '{file_name}' not found in the local record.")
        request = self.service.files().get_media(fileId=file_id)
        with open(destination_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        return destination_path
