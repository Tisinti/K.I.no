from utils import SearchMovie
import pandas as pd 

def movie_metadata(search):
    movie = SearchMovie(search).ml_match
    
    title = movie.title
    release_date = movie.release_date
    rating = movie.rating
    genre_ids = movie.genre

    return title, release_date, rating, genre_ids

def get_meta_df(rawDf: pd.DataFrame) -> pd.DataFrame:
    meta = pd.DataFrame(list(rawDf['Movie'].apply(movie_metadata)))
    meta.columns =['TMDB_Title', 'Release_Date', 'Rating', 'Genre_IDs']

    return meta

def append_meta(rawDf: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([rawDf, get_meta_df(rawDf)], axis=1)