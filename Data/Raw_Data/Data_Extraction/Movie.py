import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Movie:
    def __init__(self, metadata, index):
        self.metadata = metadata
        self.index = index
        self.title = self.get_tmdb_title()
        self.release_date = self.get_release_date()
        self.rating = self.get_letterboxd_rating()

    def __str__(self):
        return f"Titel: '{self.title}'" \
               f"\nErscheinungsdatum: {self.release_date}" \
               f"\nBewertung: {self.rating}" \
               f"\nLetterboxd Link: {self.get_link()}"

    def check_title_ambiguity(self):
        # check if there are more than 1 results
        title_list = [x['title'] for x in self.metadata]
        check = title_list.pop(self.index)
        for title in title_list:
            if check == title:
                return True
        return False

    def get_release_date(self):
        date = datetime.strptime(self.metadata[self.index]['release_date'], '%Y-%m-%d').date()
        return date

    def get_tmdb_title(self):
        title = self.metadata[self.index]['title']
        # if Title is ambiguous put release year on end of string
        if self.check_title_ambiguity():
            # first 4 digits are year (yyyy-mm-dd)
            title = title + " " + str(self.get_release_date().year)
        return title

    def get_link(self):
        # remove dots etc.
        fit = re.sub("[,./()\-;:_#'+*~?!&]", "", self.title)
        # turn everything lower case
        fit = fit.lower()
        # turn whitespaces to -
        fit = re.sub(" ", "-", fit)

        link = f'https://letterboxd.com/film/{fit}'
        return link

    def get_letterboxd_rating(self):
        print(f"A {time.process_time()}")
        url = self.get_link()
        html = requests.get(url)
        junk = BeautifulSoup(html.content, 'html.parser')

        try:
            # rating is hidden in <meta> tag named twitter:data2
            results = junk.find('meta', {"name": "twitter:data2", "content": True})
            # remove everything after first whitespace "3.5 out of 5" but we only want 3.5
            rating = re.search('\S+', results['content']).group()
            print(f"B {time.process_time()}")
            return float(rating)
        # Incase the movie does not have a rating on Letterboxd
        except Exception as e:
            return f"No Rating found! + {e}"