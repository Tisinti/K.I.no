import re
import requests
from .genre_helper import id_to_genre
from bs4 import BeautifulSoup
from datetime import datetime


class Movie:
    def __init__(self, metadata):
        self.metadata = metadata
        self.title = self.get_TMBD_title()
        self.release_date = self.get_release_date()
        self.letterboxd_link = self.get_letterboxd_link()
        self.genre = self.convert_genre_ids()
        self.rating = self.compare_ratings()

    def compare_ratings(self):
        tmdb_rating = self.get_TMDB_rating()
        #TMDB Rating should be over 0 and by more than 15 people
        if tmdb_rating > 0 and self.metadata['vote_count'] > 15:
            return tmdb_rating
        
        ltb_rating = self.get_letterboxd_rating()
        #LTB Rating should exist LULE
        if ltb_rating != None:
            return ltb_rating
        else:
            return None

    #returns the release date of the movie
    def get_release_date(self):
        return datetime.strptime(self.metadata['release_date'], '%Y-%m-%d')
    
    #returns the TMDB title 
    def get_TMBD_title(self):
        return self.metadata['title']
    
    #returns the genres IDS 
    def get_genre_id(self):
        return self.metadata['genre_ids']
    
    #convert the genre ids into readable strings
    def convert_genre_ids(self):
        genres = []
        for id in self.get_genre_id():
            genres.append(id_to_genre(id))
        return genres

    #returns formated letterboxd link of the best result
    #E.G. 'https://letterboxd.com/film/apocalypse-now'
    def get_letterboxd_link(self):
        #put everything in lowercase
        name = self.title.lower()
        # remove dots etc.
        name = re.sub("[,./()\-;:_#'+*~?!&]", "", name)
        #remove the whitespaces
        name = re.sub(" ", "-", name)
        
        return f'https://letterboxd.com/film/{name}'

    #returns the rating of the movie on letterboxed
    def get_letterboxd_rating(self):
        
        #get html code of link
        html = requests.get(self.get_letterboxd_link())
        junk = BeautifulSoup(html.content, 'html.parser')

        try:
            # rating is hidden in <meta> tag named twitter:data2
            results = junk.find('meta', {"name": "twitter:data2", "content": True})
            # remove everything after first whitespace "3.5 out of 5" but we only want 3.5
            rating = re.search('\S+', results['content']).group()
            return float(rating) * 2
        # In case the movie does not have a rating on Letterboxd
        except Exception as e:
            return None
    
    def get_TMDB_rating(self):
        return self.metadata['vote_average']