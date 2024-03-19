import json
from typing import Optional, Iterable
from utils.file_cache import file_cache_decorator
from utils.lastfm.api import _get_user_info, _get_user_top_artists


@file_cache_decorator()
def get_user_info_cached(username: str) -> str:
    return _get_user_info(username)


def username_exists(username: str) -> bool:
    if get_user_info_cached(username):
        return True


@file_cache_decorator(keep_days=1)
def get_user_top_artists_cached_one_day(username, drange=None):
    return _get_user_top_artists(username, drange)


@file_cache_decorator(keep_days=30)
def get_user_top_artists_cached_one_month(username, drange=None):
    return _get_user_top_artists(username, drange)


@file_cache_decorator(keep_days=365)
def get_user_top_artists_cached_one_year(username, drange=None):
    return _get_user_top_artists(username, drange)


def get_user_top_artists(username: str, drange: Optional[str] = None) -> Iterable:
    if drange and int(drange) < 180:
        retval = get_user_top_artists_cached_one_day(username, drange)
    elif drange and int(drange) <= 365:
        retval = get_user_top_artists_cached_one_month(username, drange)
    else:
        retval = get_user_top_artists_cached_one_year(username, drange)
    artists_with_rank = json.loads(retval)
    return [
        artist
        for artist, rank
        in artists_with_rank
    ]


def get_popular_artists(username: str, drange: str) -> Iterable[str]:
    if not username_exists(username):
        raise Exception('Username does not exist')
    return get_user_top_artists(username, drange)
