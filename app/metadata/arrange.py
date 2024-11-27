import pandas as pd
from typing import Tuple

from app.search import SearchMovie
from .add_time import add_semester, date_to_weekday, movie_age


def movie_metadata(search: str) -> Tuple[str, str, float, list, str, int, int]:
    movie = SearchMovie(search).meta

    title = movie.title
    release_date = movie.release_date
    rating = movie.rating
    genre_ids = movie.genre
    language = movie.language
    budget = movie.budget
    runtime = movie.runtime

    return title, release_date, rating, genre_ids, language, budget, runtime


def get_meta_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    meta = pd.DataFrame(list(raw_df['Titel'].apply(movie_metadata)))
    meta.columns = ['TMDB_Title', 'Release_Date', 'Rating', 'Genre',
                    'Original_Language', 'Budget', 'Runtime']

    return meta


def append_time(raw_df: pd.DataFrame) -> pd.DataFrame:
    time_df = raw_df.copy()

    time_df['Date'] = pd.to_datetime(time_df['Date']).dt.date
    time_df['Semester'] = time_df['Date'].apply(add_semester)
    time_df['Weekday'] = time_df['Date'].apply(date_to_weekday)

    return time_df


def append_meta(raw_df: pd.DataFrame) -> pd.DataFrame:
    full_df = pd.concat([raw_df, get_meta_df(raw_df)], axis=1)
    time_df = append_time(full_df)

    time_df['MovieAge'] = movie_age(time_df['Release_Date'], time_df['Date'])
    time_df.rename(columns={'Titel': 'OG_Title'}, inplace=True)

    ordered_df = time_df[['OG_Title', 'TMDB_Title', 'Release_Date', 'Rating', 'Genre',
                          'Budget', 'Runtime', 'Original_Language', 'MovieAge', 'Semester', 'Weekday',
                          'Date', 'Attendance']]

    ordered_df['Rating'] = ordered_df['Rating'].fillna(ordered_df['Rating'].mean())

    return ordered_df


def missing(clean_df: pd.DataFrame) -> pd.DataFrame:
    return clean_df[(clean_df.isna().any(axis=1)) | (clean_df['MovieAge'] <= pd.Timedelta(0))]


def clean(raw_df: pd.DataFrame) -> pd.DataFrame:
    clean_df = raw_df.dropna(how='any')
    clean_df = clean_df[clean_df['MovieAge'] >= pd.Timedelta(0)]
    clean_df = clean_df[~clean_df['OG_Title'].str.contains("sneak", case=False)]

    return clean_df
