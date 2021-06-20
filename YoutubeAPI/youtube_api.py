import logging
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]


def create_youtube_auth():
    try:
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        return googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
    except Exception as e:
        logging.error(e)
        return None


def get_playlist_data(youtube, playlist_id):
    try:
        return youtube.playlistItems().list(
            part='contentDetails, snippet',
            playlistId=playlist_id
        ).execute()
    except Exception as e:
        logging.error(e)


def get_video_info(youtube, id):
    try:
        return youtube.videos().list(
            part="snippet",
            id=id
        ).execute()
    except Exception as e:
        logging.error(e)


def insert_into_playlist(youtube, playlist_id, video_id):
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

        youtube.playlistItems().insert(
            part='snippet',
            body=video_payload
        ).execute()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    youtube = create_youtube_auth()
    insert_into_playlist(youtube, '<PLAYLIST-ID>', '<VIDEO-ID>')
