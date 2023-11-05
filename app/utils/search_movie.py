from .movie import Movie
from dotenv import load_dotenv
import requests
import os

load_dotenv()

class SearchMovie:
    def __init__(self, search):
        self.search = search
        self.API_KEY = os.getenv('TMDB_API_KEY')
        self.results = self.find_movies()
        #most likely match (first result)
        self.ml_match = Movie(self.results[0])

    def __str__(self):
        return (f"Title: {self.ml_match.title}"
        f"\nGenre: {self.ml_match.genre}"
        f"\nRelease-date: {self.ml_match.release_date.date()}"
        f"\nRating: {self.ml_match.rating}"
        f"\nLetterboxd Link: {self.ml_match.letterboxd_link}")
    
    #returns a list of dictionarys whith films that are possible results
    def find_movies(self):
        #search TMDB API over query
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={self.API_KEY}"
            f"&query={self.string_to_query()}")
        
        if not response.json()['results']:
            return self.noResults()

        #only return the results as a list
        return response.json()['results']
    
    def noResults(self):
        # If the search was not successfull turn everything Nonetype
        return [{'genre_ids': None, 'release_date': None, 'title': None, 
                'vote_average': None, 'vote_count': None, 'original_language' : None}]

    #formats a string like a query 
    def string_to_query(self):
        return self.search.replace(" ", "+")