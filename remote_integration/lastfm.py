import requests
from lxml import html

TIMEOUT = 8

session = requests.Session()
a = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('https://', a)


def filter_album_names(album_tuple_list):
    return [
        (album_name, album_year)
        for album_name, album_year in album_tuple_list
        if ' remaster)' not in album_name.lower()
        if '(deluxe edition' not in album_name.lower()
        if '(reissue)' not in album_name.lower()
        if '(re-issue)' not in album_name.lower()
        if '(bonus' not in album_name.lower()
        if '(expanded' not in album_name.lower()
    ]


def get_latest_remote_release(artist_name) -> list[str | int]:
    url = f"https://www.last.fm/music/{artist_name.replace(' ', '+')}"
    page = session.get(url, timeout=TIMEOUT).text
    doc = html.fromstring(page)
    h3 = doc.xpath("//h4[@class='artist-header-featured-items-item-header'][contains(text(),'Latest release')]/following-sibling::h3")[0]
    p = doc.xpath("//h4[@class='artist-header-featured-items-item-header'][contains(text(),'Latest release')]/following-sibling::p")[0]
    album_name = h3.text_content().strip()
    album_year = p.text_content().strip().split()[-1]
    return [album_name, int(album_year)]


def get_remote_releases(artist_name) -> list[tuple[str, int]]:
    # Just get the first two pages of the popular albums on last.fm and assume that is most of it.
    # TODO is last.fm a good source? we get a lot of non-official releases.. and no way to identify studio albums
    cleaned_albums = []
    for page in range(1, 3):
        url = f"https://www.last.fm/music/{artist_name.replace(' ', '+')}/+albums?page={page}"
        page = session.get(url, timeout=TIMEOUT).text
        doc = html.fromstring(page)
        albums = doc.xpath("//section[@id='artist-albums-section']/ol/li")
        for album in albums:
            try:
                album_name = album.xpath('div/h3/a')[0].text_content()
                album_date = album.xpath('div/p')[1].text_content().strip().split('·')[0].strip()
                album_year = album_date[-4:]
            except IndexError:
                print('error for ', album.text_content())
                continue
            if not album_year.isnumeric():
                album_year = 0
            cleaned_albums.append((album_name, int(album_year)))
    return filter_album_names(cleaned_albums)
