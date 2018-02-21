from bs4 import BeautifulSoup
from pandas import DataFrame
from re import compile, DOTALL
from requests import get


class ArtFactsArtistScraper(object):
    def __init__(self, artist_url):
        self.expos = []
        self.html = get(artist_url).text
        self.data = None

    def scrape(self):
        self.add_solo_shows()
        self.add_group_shows()
        self.add_ongoing_solo_shows()
        self.add_ongoing_groups_shows()
        self.data = DataFrame(self.expos, columns=["year", "title", "venue", "city", "type"])

    def persist_to_excel(self, filename):
        self.data.to_excel(filename)

    def get_expos(self, soup, t):
        year = 0
        for tag in soup.dl.findChildren():
            if tag.name == "dt":
                year = tag.contents[0]
            if tag.name == "dd":
                titles = tag.find("a", attrs={"title": compile("Exhibition")}).contents
                title = titles[0] if len(titles) > 0 else ""
                venue = tag.find("a", attrs={"title": compile("Venue")}).contents[0]
                city = tag.find("span", attrs={"title": "Venue City"}).contents[0]
                self.expos.append((year, title, venue, city, t))

    def add_type_of_expos(self, regex, expotype):
        solo_html_regex = compile(regex, DOTALL)
        solo_html = solo_html_regex.findall(self.html)[0]
        soup = BeautifulSoup(solo_html, "html5lib")
        self.get_expos(soup, expotype)

    def add_solo_shows(self):
        self.add_type_of_expos('<h3 id="solo">Solo shows <span>.+?</dl>', 'solo')

    def add_group_shows(self):
        self.add_type_of_expos('<h3 id="group">Group shows <span>.+?</dl>', 'group')

    def add_ongoing_solo_shows(self):
        self.add_type_of_expos('<h3>Ongoing solo exhibitions <span>.+?</dl>', 'solo')

    def add_ongoing_groups_shows(self):
        self.add_type_of_expos('<h3>Ongoing group exhibitions <span>.+?</dl>', 'group')


if __name__ == "__main__":
    afas = ArtFactsArtistScraper("http://www.artfacts.net/en/artist/jef-geys-2938")
    afas.scrape()
    afas.persist_to_excel("artfacts_jef_geys_scrape.xlsx")
