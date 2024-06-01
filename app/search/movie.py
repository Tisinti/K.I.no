import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os


class Movie:
    sn = requests.Session()

    def __init__(self, id):
        self.id = id
        self.API_KEY = os.getenv("TMDB_API_KEY")

        self.metadata = self.get_metadata()
        self.title = self.get_title()
        self.release_date = self.get_release_date()
        self.language = self.get_lan()
        self.genre = self.get_genre_id()
        self.rating = self.compare_ratings()
        self.budget = self.get_budget()
        self.runtime = self.get_runtime()

    def get_metadata(self):
        response = self.sn.get(
            f"https://api.themoviedb.org/3/movie/{self.id}?api_key={self.API_KEY}"
        )
        if "title" in response.json():
            return response.json()
        else:
            return self.no_results()

    def no_results(self) -> list[dict]:
        # If the search was not successfull turn everything Nonetype
        return {
            "genres": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "budget": None,
            "original_language": None,
            "runtime": None,
        }

    def get_runtime(self):
        return self.metadata["runtime"]

    def get_lan(self):
        return self.metadata["original_language"]

    def get_budget(self):
        return self.metadata["budget"]

    def compare_ratings(self):
        tmdb_rating = self.metadata["vote_average"]

        # In Case the Search was not successfull
        if tmdb_rating is None:
            return None

        # TMDB Rating should be over 0 and by more than 15 people
        if tmdb_rating > 0 and self.metadata["vote_count"] > 15:
            return tmdb_rating

        ltb_rating = self.get_letterboxd_rating()
        # LTB Rating should better exist LULE
        if ltb_rating is not None:
            return ltb_rating
        else:
            return None

    # returns the release date of the movie
    def get_release_date(self):
        try:
            return datetime.strptime(self.metadata["release_date"], "%Y-%m-%d").date()
        except Exception:
            return None  # In Case the Search was not successfull

    # returns the TMDB title
    def get_title(self):
        return self.metadata["title"]

    # returns the genres IDS
    def get_genre_id(self):
        if not self.metadata["genres"]:
            return None

        all = []
        for dic in self.metadata["genres"]:
            all.append(dic["name"])
        return all

    # returns formated letterboxd link of the best result
    # E.G. 'https://letterboxd.com/film/apocalypse-now'
    def get_letterboxd_link(self):
        if self.title is None:
            return  # In Case the Search was not successfull

        # put everything in lowercase
        name = self.title.lower()
        # remove dots etc.
        name = re.sub(r"[,./()\-;:_#'+*~?!&]", "", name)
        # remove the whitespaces
        name = re.sub(" ", "-", name)

        return f"https://letterboxd.com/film/{name}"

    # returns the rating of the movie on letterboxed
    def get_letterboxd_rating(self):
        # get html code of link
        html = requests.get(self.get_letterboxd_link())
        junk = BeautifulSoup(html.content, "html.parser")

        try:
            # rating is hidden in <meta> tag named twitter:data2
            results = junk.find("meta", {"name": "twitter:data2", "content": True})
            # remove everything after first whitespace "3.5 out of 5" but we only want 3.5
            rating = re.search(r"\S+", results["content"]).group()
            return float(rating) * 2
        # In case the movie does not have a rating on Letterboxd
        except Exception:
            return None
