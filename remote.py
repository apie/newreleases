#!/usr/bin/env python

import json
import requests
from lxml import html
from typing import Tuple
from file_cache import file_cache_decorator

TIMEOUT = 8

session = requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('https://', a)

@file_cache_decorator(keep_days=365)
def get_latest_remote_release(artist_name) -> str:
    url = f"https://www.last.fm/music/{artist_name.replace(' ', '+')}"
#    print(url)
    page = session.get(url, timeout=TIMEOUT).text
    doc = html.fromstring(page)
    h3 = doc.xpath("//h4[@class='artist-header-featured-items-item-header'][contains(text(),'Latest release')]/following-sibling::h3")[0]
    p = doc.xpath("//h4[@class='artist-header-featured-items-item-header'][contains(text(),'Latest release')]/following-sibling::p")[0]
    album_name = h3.text_content().strip()
    album_year = p.text_content().strip().split()[-1]
    return json.dumps([album_name, int(album_year)])

