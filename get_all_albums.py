#!/usr/bin/env python3
# By DenickM 20240227
import typer
import logging
import json
from local import MUSIC_DIR, get_local_releases
from remote import cached_get_remote_releases

try:
    with open('ignore.txt', 'r') as f:
        ignore = set(f.read().splitlines())
except FileNotFoundError:
    ignore = set()


def hashi(tuple_list):
    # Ignore special chars since there could be reasons why we removed them from local folders
    def clean(s):
        return str(s).lower()\
            .replace("’", '')\
            .replace(",", "")\
            .replace("?", "")\
            .replace("!", "")
    return map(lambda x: clean(x[1]) + '|' + clean(x[0]), tuple_list)


def iter_dirs(verbose: bool = False, filter_artist: str = ''):
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level)
    for genre in MUSIC_DIR.iterdir():
        if not genre.is_dir():
            continue
        for artist in genre.iterdir():
            if filter_artist and artist.stem.lower() != filter_artist.lower():
                continue
            if artist.stem in ignore:
                logging.info(f"Ignoring {artist.stem}")
                continue
            local_releases = get_local_releases(artist)
            yield genre, artist, local_releases


def get_it(verbose: bool = False, filter_artist: str = '', sort_on_album_count: bool = False):
    dirs = list(iter_dirs(verbose, filter_artist))
    for d in sorted(dirs, key=lambda x: len(x[2] if sort_on_album_count else x), reverse=True):
        genre, artist, local_releases = d
        print()
        logging.warning(f"Genre: {genre.stem} - Artist: {artist.stem}")
        logging.info('--Local:')
        for name, year in sorted(local_releases, key=lambda x: x[1]):
            logging.info('%s %s', year, name)
        logging.info('')
        remote_releases = json.loads(cached_get_remote_releases(artist.stem))
        logging.info('--Remote:')
        for name, year in sorted(remote_releases, key=lambda x: x[1]):
            logging.info('%s %s', year, name)
        if len(remote_releases) == 0:
            logging.error('No remote releases found!')
            if filter_artist:
                raise typer.Exit(code=1)

        if missing := set(hashi(remote_releases)).difference(set(hashi(local_releases))):
            logging.warning('--Missing the following %d releases in our local collection:', len(missing))
            for year_name in sorted(missing):
                logging.warning('%s %s', *year_name.split('|'))
            if filter_artist:
                raise typer.Exit(code=1)
        else:
            logging.info('Your collection is complete!')
        logging.info('')


if __name__ == '__main__':
    typer.run(get_it)
