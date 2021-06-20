import logging
import os
import googleapiclient.errors
import googleapiclient.discovery
import google_auth_oauthlib.flow

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


class YoutubeAPI:
    def __init__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    def get_playlist_data(self, playlist_id):
        try:
            return self.youtube.playlistItems().list(
                part='contentDetails, snippet',
                playlistId=playlist_id
            ).execute()
        except Exception as e:
            logging.error(e)

    def get_video_info(self, id):
        try:
            return self.youtube.videos().list(
                part="snippet",
                id=id
            ).execute()
        except Exception as e:
            logging.error(e)

    def insert_into_playlist(self, playlist_id, video_id):
        try:
            # response = get_video_info(youtube, video_id)
            video_payload = {
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }

            self.youtube.playlistItems().insert(
                part='snippet',
                body=video_payload
            ).execute()
            logging.info("Resource added to the playlist")
        except Exception as e:
            logging.error(e)
