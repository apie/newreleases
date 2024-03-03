import musicbrainzngs
from datetime import datetime
import logging

logging.getLogger('musicbrainzngs').setLevel(logging.WARNING)

musicbrainzngs.set_useragent("Apie newreleases", 1)


def get_artist_id(artist_name: str) -> str:
    artist = musicbrainzngs.search_artists(artist_name)['artist-list'][0]
    assert artist['ext:score'] == '100'
    return artist['id']


def get_remote_releases(artist_name) -> list[tuple[str, int]]:
    try:
        artist_id = get_artist_id(artist_name)
    except IndexError:
        return []
    release_groups = musicbrainzngs.browse_release_groups(artist=artist_id, release_type='album')['release-group-list']
    cleaned_albums = []
    for release_group in release_groups:
        if release_group['type'] != 'Album':
            continue  # Skips live albums and compilations
        album_name = release_group['title']
        try:
            release_date = datetime.fromisoformat(release_group['first-release-date'])
            release_year = release_date.year
        except ValueError:
            try:
                release_year = int(release_group['first-release-date'][:4])
            except ValueError:
                release_year = 0

        cleaned_albums.append((album_name, release_year))
    return cleaned_albums


def get_latest_remote_release(artist_name) -> list[str | int]:
    album_name, album_year = get_remote_releases(artist_name)[-1]
    return [album_name, int(album_year)]
