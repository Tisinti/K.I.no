import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.preprocessing import OneHotEncoder, StandardScaler

load_dotenv()


def get_full() -> pd.DataFrame:
    return pd.read_csv(os.getenv('FULL_CSV'), parse_dates=['Release_Date', 'Date']).drop("Unnamed: 0", axis=1)


def get_after_covid() -> pd.DataFrame:
    full = get_full()
    return full[full['Date'] > pd.to_datetime('2020-03-01')]


def preprocess(df: pd.DataFrame, fit: bool, enc: OneHotEncoder, scaler: StandardScaler) -> pd.DataFrame:
    df = prettify_df(df)
    df = explode_genre(df)
    if fit:
        df[['Genre', 'Original_Language', 'Semester', 'Weekday']] = enc.fit_transform(
            df[['Genre', 'Original_Language', 'Semester', 'Weekday']])
        att, df = df['Attendance'], scaler.fit_transform(df.loc[:, df.columns != 'Attendance'])
        df = pd.concat([df, att], axis=1)
    else:
        df[['Genre', 'Original_Language', 'Semester', 'Weekday']] = enc.transform(
            df[['Genre', 'Original_Language', 'Semester', 'Weekday']])
        att, df = df['Attendance'], scaler.transform(df.loc[:, df.columns != 'Attendance'])
        df = pd.concat([df, att], axis=1)
    return df


def drop_names(full: pd.DataFrame) -> pd.DataFrame:
    full['Semester'] = full['Semester'].str.split(" ").str[0]
    return full.drop(['OG_Title', 'TMDB_Title'], axis=1)


def explode_genre(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df['Genre'].iloc[0], list):
        df['Genre'] = df['Genre'].apply(lambda x: x[1:-1].replace(' ', '').replace("'", '').split(','))
    df = df.explode('Genre')
    return df


def convert_delta(df: pd.DataFrame) -> pd.DataFrame:
    df['MovieAge'] = pd.to_timedelta(df['MovieAge']).dt.days
    return df


def explode_showndate(df: pd.DataFrame) -> pd.DataFrame:
    df['ShownYear'] = df['Date'].dt.year
    return df.drop('Date', axis=1)


def prettify_df(raw: pd.DataFrame) -> pd.DataFrame:
    pretty = raw.reset_index(drop=True)
    pretty = drop_names(pretty)
    pretty = pretty.drop('Release_Date', axis=1)
    pretty = convert_delta(pretty)
    pretty = explode_showndate(pretty)
    return pretty.reset_index(drop=True)
