import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

API_KEY = "999ff2a141d82575eae2cd20f2aad315"


class MovieSearch:
    def __init__(self, search):
        self.search = search
        self.movie_metadata_list = self.find_movie()
        self.most_likely_movie = Movie(self.movie_metadata_list, 0)

    def find_movie(self):
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}"
            f"&query={self.string_to_query()}")
        return response.json()['results']

    def string_to_query(self):
        return self.search.replace(" ", "+")

    def get_movie(self, index):
        return Movie(self.movie_metadata_list, index)


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
        if len(self.metadata) > 1:
            # count each time the title mirrors the search
            # this process could be parallelized but not looking into that right now
            # also i hate myself for implementing it this way, seems so clunky
            count = 0
            for movie in self.metadata:
                if self.metadata[self.index]['title'] == movie['title']:
                    count += 1
            # count is at least 1 because the search title is always in the list itself
            if count > 1:
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
        url = self.get_link()
        html = requests.get(url)
        junk = BeautifulSoup(html.content, 'html.parser')

        try:
            # rating is hidden in <meta> tag named twitter:data2
            results = junk.find('meta', {"name": "twitter:data2", "content": True})
            # remove everything after first whitespace "3.5 out of 5" but we only want 3.5
            rating = re.search('\S+', results['content']).group()
            return float(rating)
        # Incase the movie does not have a rating on Letterboxd
        except Exception as e:
            return f"No Rating found! + {e}"


if __name__ == "__main__":
    search_result = MovieSearch("Red Rocket")
    print(search_result.get_movie(0))
