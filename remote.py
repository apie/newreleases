import json
from file_cache import file_cache_decorator
from remote_integration.musicbrainz import get_latest_remote_release
from remote_integration.musicbrainz import get_remote_releases


@file_cache_decorator(keep_days=365)
def cached_get_latest_remote_release(artist_name) -> str:
    rl = get_latest_remote_release(artist_name)
    return json.dumps(rl)


@file_cache_decorator(keep_days=365)
def cached_get_remote_releases(artist_name) -> str:
    rls = get_remote_releases(artist_name)
    return json.dumps(rls)
