from app.search import SearchMovie
from .add_time import add_semester, date_to_weekday, movie_age
import pandas as pd 


def movie_metadata(search):
    movie = SearchMovie(search).meta
    
    title = movie.title
    release_date = movie.release_date
    rating = movie.rating
    genre_ids = movie.genre
    lan = movie.language
    budget = movie.budget
    runtime = movie.runtime

    return title, release_date, rating, genre_ids, lan, budget, runtime

def get_meta_df(rawDf: pd.DataFrame) -> pd.DataFrame:
    meta = pd.DataFrame(list(rawDf['Titel'].apply(movie_metadata)))
    meta.columns =['TMDB_Title', 'Release_Date', 'Rating', 'Genre', 
                   'Original_Language', 'Budget', 'Runtime']

    return meta

def append_time(rawDf: pd.DataFrame):
    timeDf = rawDf

    timeDf['Date'] = pd.to_datetime(timeDf['Date']).dt.date
    timeDf['Semester'] = timeDf['Date'].apply(add_semester)
    timeDf['Weekday'] = timeDf['Date'].apply(date_to_weekday)
    return timeDf

def append_meta(rawDf: pd.DataFrame) -> pd.DataFrame:
    pd.set_option('future.no_silent_downcasting', True)    
    
    full = pd.concat([rawDf, get_meta_df(rawDf)], axis=1)
    time = append_time(full)

    time['MovieAge'] = movie_age(time['Release_Date'], time['Date'])

    time.rename(columns = {'Titel':'OG_Title'}, inplace = True)    
    
    # orderd Okayeg
    orderd = time[['OG_Title','TMDB_Title', 'Release_Date', 'Rating', 'Genre', 
                'Budget', 'Runtime', 'Original_Language', 'MovieAge', 'Semester', 'Weekday', 
                'Date', 'Attendance']]
    # Fill na Ratings with mean of the Semester
    orderd['Rating'] = orderd['Rating'].fillna(orderd['Rating'].mean())

    return orderd

def missing(cleanDf: pd.DataFrame) -> pd.DataFrame:
    return  cleanDf[(cleanDf.isna().any(axis=1)) | (cleanDf['MovieAge'] <= pd.Timedelta(0))]

def clean(rawDf: pd.DataFrame) -> pd.DataFrame:
    cleanDf = rawDf

    #Currently cleaning during iteration
    cleanDf = cleanDf.dropna(how='any')
    # Throw out movies that have come out after being shown (wrong search result)
    cleanDf = cleanDf[cleanDf['MovieAge'] >= pd.Timedelta(0)]
    # Throw out Sneaks
    cleanDf = cleanDf[~cleanDf['OG_Title'].str.contains("sneak", case=False)]

    return cleanDf