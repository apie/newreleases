#!/usr/bin/env python3
# Checks latest release for each artist.
# By DenickM 20210724
from pathlib import Path
from typing import Tuple, List

MUSIC_DIR = Path().home() / 'muziek'


def get_local_releases(artist_path: Path) -> List[Tuple[str, int]]:
    releases = []
    for local_release in artist_path.iterdir():
        album = local_release.stem
        if len(album) < 5 or not (album[:4].isnumeric() and album[4] == ' '):
            # print(f'unrecognized year for local album {album}')
            pass
        else:
            year, name = album.split(' ', maxsplit=1)
            releases.append((name, int(year)))
    return releases


def get_latest_local_release(artist_path: Path) -> Tuple[str, int]:
    try:
        return sorted(get_local_releases(artist_path), key=lambda x: x[1])[-1]
    except IndexError:
        return ('', 0)
