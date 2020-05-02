import io
import os

import google
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import json

from googleapiclient.http import MediaIoBaseDownload

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


class CaptionDownload():

    def __init__(self, client_secrets_file: str) -> None:
        self.client_secrets_file = client_secrets_file
        with open(client_secrets_file) as f:
            self.clientSecret = json.load(f)['installed']

    def refreshToken(self):
        params = {
            "grant_type": "refresh_token",
            "client_id": self.clientSecret['client_id'],
            "client_secret": self.clientSecret['client_secret'],
            "refresh_token": self.clientSecret['refresh_token']
        }

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
            return r.json()['access_token']
        else:
            return None

    def download(self, videoID, output_file='caption.vtt'):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # TODO: eliminare in prod

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        credentials = None
        if "refresh_token" in self.clientSecret:
            access_token = self.refreshToken()
            credentials = google.oauth2.credentials.Credentials(access_token)

        # If is none i request a new credential, browser is needed
        if credentials is None:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, scopes)
            credentials = flow.run_console()
            self.clientSecret['refresh_token'] = credentials.refresh_token
            with open(self.client_secrets_file, 'w') as f:
                json.dump({'installed': self.clientSecret}, f)

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        requestCaptionID = youtube.captions().list(
            part="id",
            videoId=videoID
        )
        response = requestCaptionID.execute()
        captionID = response['items'][0]['id']

        request = youtube.captions().download(
            id=captionID,
            tfmt="vtt"
        )

        fh = io.FileIO('Outputs/' + output_file, "wb")

        download = MediaIoBaseDownload(fh, request)
        complete = False
        while not complete:
            status, complete = download.next_chunk()
