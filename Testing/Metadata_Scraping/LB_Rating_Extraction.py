import requests
from bs4 import BeautifulSoup
import re

API_KEY = "999ff2a141d82575eae2cd20f2aad315"

def find_movie(movie):
    response = requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}"
        f"&query={string_to_query(movie)}")
    return response.json()['results']

def string_to_query(title):
    return title.replace(" ", "+")


def check_title_ambiguity(results):
    if len(results) > 1:                #check if there are more than 1 results
        for i in range(len(results)-1): #check if the title of the first movie is equal to other results
            if results[0]['title'] == results[i+1]['title']: #range from 0 to length of results - 1. Start with second result.
                return True
    return False


def get_release_date(results):
    return results[0]['release_date']


def get_tmdb_title(results):
    title = results[0]['title']
    if check_title_ambiguity(results):                          #if Title is ambigues put realease year on end of string
        title = title + " " + get_release_date(results)[:4]     #first 4 digits are year (yyyy-mm-dd)
    return title


def title_to_link(tmdb_title):
    fit = re.sub("[,./()\-;:_#'+*~?!]", "", tmdb_title)      # remove dots etc.
    fit = fit.lower()                                       # turn everything lower case
    fit = re.sub(" ", "-", fit)                             # turn whitespaces to -

    link = f'https://letterboxd.com/film/{fit}'
    return link


def get_letterboxd_rating(title):
    url = title_to_link(get_tmdb_title(find_movie(title)))
    html = requests.get(url)
    junk = BeautifulSoup(html.content, 'html.parser')

    try:
        results = junk.find('meta', {"name": "twitter:data2", "content": True})
        rating = re.search('\S+', results['content']).group()
        return rating
    except Exception as e:   #Incase the movie does not have a rating on Letterboxd
        return f"No Rating found! + {e}"



if __name__ == "__main__":
    name = "The Matrix"
    print(get_letterboxd_rating(name))
    print(title_to_link(get_tmdb_title(find_movie(name))))