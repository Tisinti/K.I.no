import os
import re
from datetime import datetime
from typing import List, Union, Optional, Dict

import requests
from bs4 import BeautifulSoup


class Movie:
    sn = requests.Session()

    def __init__(self, movie_id: int) -> None:
        self.id = movie_id
        self.API_KEY = os.getenv('TMDB_API_KEY')

        self.metadata = self.get_metadata()
        self.title = self.get_title()
        self.release_date = self.get_release_date()
        self.language = self.get_language()
        self.genre = self.get_genre_id()
        self.rating = self.compare_ratings()
        self.budget = self.get_budget()
        self.runtime = self.get_runtime()

    def get_metadata(self) -> Dict[str, Union[str, float, int, None]]:
        response = self.sn.get(f"https://api.themoviedb.org/3/movie/{self.id}?api_key={self.API_KEY}")
        if 'title' in response.json():
            return response.json()
        else:
            return self.no_results()

    def no_results(self) -> Dict[str, Optional[Union[str, int, float]]]:
        # If the search was not successful, return a dict with None values
        return {
            'genres': None,
            'release_date': None,
            'title': None,
            'vote_average': None,
            'vote_count': None,
            'budget': None,
            'original_language': None,
            'runtime': None
        }

    def get_runtime(self) -> Optional[int]:
        return self.metadata.get('runtime')

    def get_language(self) -> Optional[str]:
        return self.metadata.get('original_language')

    def get_budget(self) -> Optional[int]:
        return self.metadata.get('budget')

    def compare_ratings(self) -> Optional[float]:
        tmdb_rating = self.metadata.get('vote_average')

        # In case the search was not successful
        if tmdb_rating is None:
            return None

        # TMDB rating should be over 0 and by more than 15 people
        if tmdb_rating > 0 and self.metadata.get('vote_count', 0) > 15:
            return tmdb_rating

        ltb_rating = self.get_letterboxd_rating()
        # LTB rating should better exist
        if ltb_rating is not None:
            return ltb_rating
        else:
            return None

    def get_release_date(self) -> Optional[datetime.date]:
        try:
            return datetime.strptime(self.metadata['release_date'], '%Y-%m-%d').date()
        except Exception:
            return None  # In case the search was not successful

    def get_title(self) -> Optional[str]:
        return self.metadata.get('title')

    def get_genre_id(self) -> Optional[List[str]]:
        if not self.metadata['genres']:
            return None

        return [genre['name'] for genre in self.metadata['genres']]

    def get_letterboxd_link(self) -> Optional[str]:
        if self.title is None:
            return None  # In case the search was not successful

        # Put everything in lowercase and remove unwanted characters
        name = re.sub(r"[,./()\-;:_#'+*~?!&]", "", self.title.lower())
        # Remove the whitespaces
        name = re.sub(r" ", "-", name)

        return f'https://letterboxd.com/film/{name}'

    def get_letterboxd_rating(self) -> Optional[float]:
        link = self.get_letterboxd_link()
        if link is None:
            return None

        # Get HTML code of link
        html = requests.get(link)
        soup = BeautifulSoup(html.content, 'html.parser')

        try:
            # Rating is hidden in <meta> tag named twitter:data2
            result = soup.find('meta', {"name": "twitter:data2", "content": True})
            if result:
                # Remove everything after the first whitespace "3.5 out of 5" but we only want 3.5
                rating = re.search(r'\S+', result['content']).group()
                return float(rating) * 2
            return None
        except Exception:
            return None  # In case the movie does not have a rating on Letterboxd
