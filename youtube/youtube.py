from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from youtube.video import Video, Playlist

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def get_playlist(playlist_id, secrets_file_path):
    youtube = _get_authenticated_service(secrets_file_path)
    try:
        return _get_playlist(playlist_id, youtube)
    except Exception as e:
        print("An HTTP error occurred:\n%s" % (e))


# Authorize the request and store authorization credentials.
def _get_authenticated_service(secrets_file_path):
    flow = InstalledAppFlow.from_client_secrets_file(secrets_file_path, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def _get_playlist(uploads_playlist_id, youtube):
    playlist_info = youtube.playlists().list(
        part="snippet", id=uploads_playlist_id
    ).execute()

    if len(playlist_info["items"]) < 1:
        return None

    list_name = playlist_info["items"][0]["snippet"]["title"]
    videos = _get_videos(uploads_playlist_id, youtube)

    playlist = Playlist(list_name)
    playlist.videos.extend(videos)
    return playlist


def _get_videos(uploads_playlist_id, youtube):
    playlistitems_request = youtube.playlistItems().list(
        playlistId=uploads_playlist_id, part="snippet", maxResults=5
    )
    videos = []
    while playlistitems_request:
        playlistitems_response = playlistitems_request.execute()
        playlist_items = playlistitems_response["items"]
        if len(playlist_items) < 1:
            break

        video_ids = playlist_items[0]["snippet"]["resourceId"]["videoId"]
        for playlist_item in playlist_items[1:]:
            video_id = playlist_item["snippet"]["resourceId"]["videoId"]
            video_ids = f"{video_ids},{video_id}"

        videos_info = youtube.videos().list(
            part="snippet,contentDetails,statistics", id=video_ids
        ).execute()

        for video_info in videos_info["items"]:
            videos.append(Video(video_info))

        playlistitems_request = youtube.playlistItems().list_next(
            playlistitems_request, playlistitems_response
        )
    return videos
