from dateutil.parser import parse
import isodate

YOU_TUBE_URL = "https://www.youtube.com"


def _get_video_url(vide_id):
    return f"{YOU_TUBE_URL}/watch?v={vide_id}"


class Video(object):
    def __init__(self, video_item):
        self.id = video_item["id"]
        self.url = _get_video_url(self.id)
        self.duration = isodate.parse_duration(video_item["contentDetails"]["duration"])
        self.stats = VideoStats(video_item["statistics"])

        video_snippet = video_item["snippet"]
        self.description = video_snippet["description"]
        self.title = video_snippet["title"]
        self.thumbnail_url = video_snippet["thumbnails"]["default"]["url"]
        self.tags = video_snippet["tags"] if "tags" in video_snippet else []
        self.published = parse(video_snippet["publishedAt"])


class VideoStats(object):
    def __init__(self, video_stats):
        self.dislikes = 0
        if "dislikeCount" in video_stats:
            self.dislikes = video_stats["dislikeCount"]
        self.favorites = 0
        if "favoriteCount" in video_stats:
            self.favorites = video_stats["favoriteCount"]
        self.likes = 0
        if "likeCount" in video_stats:
            self.likes = video_stats["likeCount"]
        self.views = 0
        if "viewCount" in video_stats:
            self.views = video_stats["viewCount"]


class Playlist(object):
    def __init__(self, name):
        self.name = name
        self.videos = []
