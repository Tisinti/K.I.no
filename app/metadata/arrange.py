from app.utils import SearchMovie
from .add_time import *
import pandas as pd 

def movie_metadata(search):
    movie = SearchMovie(search).ml_match
    
    title = movie.title
    release_date = movie.release_date
    rating = movie.rating
    genre_ids = movie.genre

    return title, release_date, rating, genre_ids

def get_meta_df(rawDf: pd.DataFrame) -> pd.DataFrame:
    meta = pd.DataFrame(list(rawDf['Titel'].apply(movie_metadata)))
    meta.columns =['TMDB_Title', 'Release_Date', 'Rating', 'Genre_IDs']

    return meta

def append_time(rawDf: pd.DataFrame):
    timeDf = rawDf

    timeDf['Date'] = timeDf['Date'].apply(str_to_date)
    timeDf['Semester'] = timeDf['Date'].apply(add_semester)
    timeDf['Weekday'] = timeDf['Date'].apply(date_to_weekday)
    return timeDf

def append_meta(rawDf: pd.DataFrame) -> pd.DataFrame:
    full = pd.concat([rawDf, get_meta_df(rawDf)], axis=1)
    time = append_time(full)

    time['MovieAge'] = movie_age(time['Release_Date'], time['Date'])

    time.rename(columns = {'Titel':'OG_Title'}, inplace = True)    

    orderd = time[['OG_Title','TMDB_Title', 'Release_Date', 'Rating', 'Genre_IDs', 
               'MovieAge', 'Semester', 'Weekday', 'Date', 'Attendance']]
    return orderd

def clean(rawDf: pd.DataFrame) -> pd.DataFrame:
    cutDf = append_meta(rawDf)
    cleanDf = cutDf.dropna(how='any')
    # Throw out movies that have come out after being shown (wrong search result)
    cleanDf = cleanDf[cleanDf['MovieAge'] >= pd.Timedelta(0)]

    return cleanDf