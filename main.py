from progressbar import printProgressBar
from youtube.youtube import get_playlist
from youtube.video_score import get_worth_score
from trello_client import get_trello_board
import os


YOUTUBE_CLIENT_SECRETS_FILE = "client_secret.json"
SCORE_PRECISION = 4
TRELLO_API_KEY = os.environ["TRELLO_API_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]


def create_list(videos, target_board, list_name):
    trello_list = target_board.add_list(list_name)
    print("Addind cards...")
    videos_count = len(videos)
    for video_index in range(videos_count):
        video = videos[video_index]
        card_title = _create_card_title(video)
        card = trello_list.add_card(card_title, video.description)

        card.attach(name="thumb", url=video.thumbnail_url)
        card.attach(name="link", url=video.url)

        duration_minutes = int(video.duration.seconds / 60)
        checklist_items = _create_checklist_items(video.url, duration_minutes, 6)
        card.add_checklist("watched", checklist_items)
        printProgressBar(video_index + 1, videos_count, prefix="Progress:", suffix="Complete", length=100)
    print(f"\n{videos_count} cards have been added")


def _score_to_alpha(score, size):
    score_str = str(int(score * 10 ** 4)).rjust(size, "0")
    aplpha = {
        "9": "A",
        "8": "B",
        "7": "C",
        "6": "D",
        "5": "E",
        "4": "F",
        "3": "G",
        "2": "H",
        "1": "I",
        "0": "J",
        " ": "J",
    }
    result = []
    for ch in score_str:
        result.append(aplpha[ch])
    return "".join(result)[:size]


def _create_checklist_items(url, duration_min, freq_min):
    items = []
    for stop in range(freq_min, duration_min + freq_min, freq_min):
        start = stop - freq_min
        item = "[{:2}:00-{:2}:00]({}&t={}m00s)".format(start, stop, url, start)
        items.append(item)
    return items


def _create_card_title(video):
    score = get_worth_score(video)
    alpha_score = _score_to_alpha(score, SCORE_PRECISION)
    title = f"{alpha_score} {video.duration} {score} {video.title}"
    return title


if __name__ == "__main__":
    trello_board_name = "you tubE test"
    playlist_id = "PLIkQ3LygyVDygwOWvF-aOKgf_7CpMrps7"
    
    pl = get_playlist(playlist_id, YOUTUBE_CLIENT_SECRETS_FILE)

    trello_board = get_trello_board(trello_board_name, TRELLO_API_KEY, TRELLO_TOKEN)
    if trello_board is None:
        raise ValueError(f'Board: "{trello_board_name}" not found!')

    publish_years = set(map(lambda v: v.published.year, pl.videos))

    for publish_year in publish_years:
        board_list_name = f"{pl.name} {publish_year}"
        videos = filter(lambda v: v.published.year == publish_year, pl.videos)
        create_list(list(videos), trello_board, board_list_name)
