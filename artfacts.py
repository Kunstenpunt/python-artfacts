from json import loads, dump, load
from pandas import DataFrame
from re import compile, DOTALL
from requests import get
from fake_useragent import UserAgent
from codecs import open
from time import sleep
from random import randint


class ArtFactsArtistScraper(object):
    def __init__(self):
        with open("artfacts_artists.json", "r", "utf-8") as f:
            self.artists = load(f)
        self.data = None
        self.base_url = "https://artfacts.net/api/v0/"
        self.ua = UserAgent()

    def get_artists(self):
        bu = self.base_url + "artists/"
        for i in range(1, 702500):
            print(i)
            bu_i = bu + str(i)
            headers = {'user-agent': self.ua.random}
            r = get(bu_i, headers=headers)
            if r.status_code == 200:
                text = r.text
                d = loads(text)
                self.artists.append(d)
                self.persist()
            sleep(randint(3, 10))

    def persist(self):
        with open("artfacts_artists.json", "w", "utf-8") as f:
            dump(self.artists, f, indent=4)


if __name__ == "__main__":
    afas = ArtFactsArtistScraper()
    afas.get_artists()
