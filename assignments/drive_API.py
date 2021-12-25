from __future__ import print_function
import io
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def download_file(service, file_id, name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    fh.seek(0)

    with io.open(os.path.join('./', name), 'wb') as f:
        f.write(fh.read())
        f.close()

def upload_file(service, name, dir, type):
    file_metadata = {'name': name}
    media = MediaFileUpload(os.path.join(dir, name), mimetype=type)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

def share_with_email(service, file_id, email):
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)

    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email
    }
    batch.add(service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
    ))
    domain_permission = {
        'type': 'domain',
        'role': 'reader',
        'domain': 'example.com'
    }
    batch.add(service.permissions().create(
            fileId=file_id,
            body=domain_permission,
            fields='id',
    ))
    batch.execute()


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'web-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

    service = build('drive', 'v3', credentials=creds)

    # uncomment one of these lines for the desired task
    # the super long string is the file id, it should be in the url for the file
    # the file needs a name, directory path, and type (jpg, pdf, etc.)
    # obviously add an email for the sharing
    # you need to have the file name that you want to download as, in this case it's "download_this.jpg"

    # upload_file(service, "screenshot.jpg", "./", 'image/jpeg')
    
    share_with_email(service, "1qD1EnOeNe16AdGgvzboHmeTCw936AbAc", "wmb8yt@virginia.edu")

    # download_file(service, "1qD1EnOeNe16AdGgvzboHmeTCw936AbAc", "download_this.jpg")

    return "items"
