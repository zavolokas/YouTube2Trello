from datetime import datetime


def get_worth_score(video):
    published = video.published.replace(tzinfo=None)
    days = float((datetime.today() - published).days)

    likes = float(video.stats.likes)
    favs = float(video.stats.favorites)
    dislikes = float(video.stats.dislikes)
    views = float(video.stats.views)

    lpd = likes / days
    fpd = favs / days
    dpd = dislikes / days

    total_ratings = lpd + fpd + dpd
    lds = ((lpd + fpd - dpd) / total_ratings + 1) / 2 if total_ratings > 0.0 else 0.0

    por = (likes + favs + dislikes) / views if views > 0.0 else 0.0
    score = lds * por
    return score