import time

from Movie import Movie
import requests

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
