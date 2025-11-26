#!/usr/bin/env python3
# Query your music dir and find for each artist the latest album you have. Then check online if there is a newer one.
# Requires your music dir to have the following structure:
# - genre
#       - artist
#           - year albumname
#               ''
#
# By DenickM 20210724
import typer
import logging
import json
from local import MUSIC_DIR, get_latest_local_release
from remote import cached_get_latest_remote_release

try:
    with open('ignore.txt', 'r') as f:
        ignore = set(f.read().splitlines())
except FileNotFoundError:
    ignore = set()


def get_it(verbose: bool = False, filter_artist: str = ''):
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level)
    logging.info('Verbose logging enabled')
    if filter_artist:
        logging.info('Filtering on artist: %s', filter_artist)
    for genre in MUSIC_DIR.iterdir():
        if not genre.is_dir():
            continue
        for artist in genre.iterdir():
            if filter_artist and artist.stem != filter_artist:
                continue
            if artist.stem in ignore:
                logging.info(f"Ignoring {artist.stem}")
                continue
            logging.info(f"Genre: {genre.stem} - Artist: {artist.stem}")
            latest_name, latest_year = get_latest_local_release(artist)
            if latest_year > 0:
                logging.info(f"Latest local release for {artist.stem}: {latest_year} {latest_name}")
                try:
                    r_latest_name, r_latest_year = json.loads(cached_get_latest_remote_release(artist.stem))
                except IndexError:
                    logging.error(f'No latest release for "{artist.stem}" found online')
                    if filter_artist:
                        raise typer.Exit(code=1)
                else:
                    if r_latest_year > latest_year:
                        logging.warning(f'Found newer release for "{artist.stem}" online: {r_latest_year} {r_latest_name}')
                        if filter_artist:
                            raise typer.Exit(code=1)
                    else:
                        logging.info('You have the latest available release')
                    logging.info('')


if __name__ == '__main__':
    typer.run(get_it)
