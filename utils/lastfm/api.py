import json
import requests
from typing import Optional


from config import LASTFM_API_KEY as API_KEY

session = requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=3)
session.mount("https://", a)

API_PERIOD = {
    None: 'overall',
    '': 'overall',
    '7': '7day',
    '30': '1month',
    '90': '3month',
    '180': '6month',
    '365': '12month',
}
MAX_ITEMS = 20
TIMEOUT = 8


def _get_user_top_artists(
    username: str, drange: Optional[str] = None
) -> str:  # returns json
    url = None
    p = API_PERIOD[drange]
    url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={API_KEY}&period={p}&format=json&limit={MAX_ITEMS}"
    print("Getting " + url.replace(API_KEY, 'SECRET'))
    resp = session.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    j = resp.json()
    # Dump as json so we can cache it to disk
    return json.dumps(
        [
            (
                top['name'],
                top['@attr']['rank'],
            )
            for top in j['topartists']['artist']
        ]
    )


def _get_user_info(username):
    url = f'http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={API_KEY}&format=json'
    print("Getting " + url.replace(API_KEY, 'SECRET'))
    resp = session.get(url, timeout=TIMEOUT)
    if resp.status_code == 404:
        return ''
    # Dump json as text so we can cache it to disk
    return resp.text
