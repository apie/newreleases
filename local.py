#!/usr/bin/env python3
# Checks latest release for each artist.
# By DenickM 20210724
from pathlib import Path
from typing import Tuple

MUSIC_DIR = Path().home() / 'muziek'

def get_latest_local_release(artist_path: Path) -> Tuple[str, int]:
    latest_release = ('', 0)
    for local_release in artist_path.iterdir():
        album = local_release.stem
        if len(album) < 5 or not (album[:4].isnumeric() and album[4] == ' '):
            # print(f'unrecognized year for local album {album}')
            pass
        else:
            year, name = album.split(' ', maxsplit=1)
            year = int(year)
            if year > latest_release[1]:
                latest_release = name, year
    return latest_release