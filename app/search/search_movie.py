import os
from typing import List, Dict

import requests
from dotenv import load_dotenv

from .movie import Movie

load_dotenv()


class SearchMovie:
    sn = requests.Session()

    def __init__(self, search: str) -> None:
        self.search = search
        self.API_KEY = os.getenv('TMDB_API_KEY')
        self.results = self.find_movies()
        # Most likely match (first result)
        self.meta = Movie(self.results[0]['id'])

    def __str__(self) -> str:
        return (f"Title: {self.meta.title}"
                f"\nGenre: {self.meta.genre}"
                f"\nBudget: {self.meta.budget}"
                f"\nRelease-date: {self.meta.release_date}"
                f"\nRuntime: {self.meta.runtime}"
                f"\nRating: {self.meta.rating}")

    # Returns a list of dictionaries with films that are possible results
    def find_movies(self) -> List[Dict]:
        # Search TMDB API over query
        response = self.sn.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}"
            f"&query={self.string_to_query()}")

        if not response.json().get('results'):
            return self.no_results()

        # Only return the results as a list
        return response.json()['results']

    def no_results(self) -> List[Dict]:
        # If the search was not successful, return a dict with None values
        return [{'id': 0}]

    # Formats a string like a query
    def string_to_query(self) -> str:
        return self.search.replace(" ", "+")
