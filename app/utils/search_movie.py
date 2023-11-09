from .movie import Movie
from dotenv import load_dotenv
import requests
import os

load_dotenv()

class SearchMovie:
    sn = requests.Session()

    def __init__(self, search: str) -> None:
        self.search = search
        self.API_KEY = os.getenv('TMDB_API_KEY')
        self.results = self.find_movies()
        #most likely match (first result)
        self.meta = Movie(self.results[0]['id'])

    def __str__(self) -> None:
        return (f"Title: {self.meta.title}"
        f"\nGenre: {self.meta.genre}"
        f"\nBudget: {self.meta.budget}"
        f"\nRelease-date: {self.meta.release_date}"
        f"\nRuntime: {self.meta.runtime}"
        f"\nRating: {self.meta.rating}")
    
    #returns a list of dictionarys whith films that are possible results
    def find_movies(self) -> list[dict]:
        #search TMDB API over query
        response = self.sn.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}"
            f"&query={self.string_to_query()}")
        
        if not response.json()['results']:
            return self.no_results()

        #only return the results as a list
        return response.json()['results']
    
    def no_results(self) -> list[dict]:
        # If the search was not successfull turn everything Nonetype
        return [{'id': 0}]

    #formats a string like a query 
    def string_to_query(self) -> str:
        return self.search.replace(" ", "+")