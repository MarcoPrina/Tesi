import os

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class PlaylistData():

    def __init__(self, credentials) -> None:
        self.credentials = credentials

    def get(self, playlistID):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # TODO: eliminare in prod

        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=self.credentials)

        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=50,
            playlistId=playlistID
        )
        return request.execute()


