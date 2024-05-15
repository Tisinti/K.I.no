import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


def get_full() -> pd.DataFrame:
    return pd.read_csv(os.getenv('FULL_CSV'),
                       parse_dates=['Release_Date', 'Date']).drop("Unnamed: 0", axis=1)

def get_after_covid() -> pd.DataFrame:
    full =  get_full()
    return full[full['Date'] > pd.to_datetime('2020-3-1')]

def preprocess(df: pd.DataFrame, fit: bool, enc, scaler) -> pd.DataFrame:
    df = prettify_df(df)
    df = explode_genre(df)
    if fit:
        df[['Genre', 'Original_Language', 'Semester', 'Weekday']] = enc.fit_transform(df[['Genre', 'Original_Language', 'Semester', 'Weekday']])
        att, df = df['Attendance'], scaler.fit_transform(df.loc[:, df.columns != 'Attendance'])
        df = pd.concat([df, att], axis=1)
    else:
        df[['Genre', 'Original_Language', 'Semester', 'Weekday']] = enc.transform(df[['Genre', 'Original_Language', 'Semester', 'Weekday']])
        att, df = df['Attendance'], scaler.transform(df.loc[:, df.columns != 'Attendance'])
        df = pd.concat([df, att], axis=1)
    return df 

def drop_names(full: pd.DataFrame) -> pd.DataFrame:
    full['Semester'] = full['Semester'].str.split(" ").str[0]
    return full.drop(['OG_Title', 'TMDB_Title'], axis = 1)

def explode_genre(final: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(final['Genre'][0], list):
        final['Genre'] = final['Genre'].apply(lambda x: x[1:-1].replace(' ', '').replace("'", '').split(','))
    final = final.explode('Genre')
    return final

def convert_delta(final: pd.DataFrame) -> pd.DataFrame:
    final['MovieAge'] = pd.to_timedelta(final['MovieAge']).dt.days
    return final

def explode_showndate(final: pd.DataFrame) -> pd.DataFrame:
    shown = final['Date']
    final['ShownYear'] = shown.dt.year
    return final.drop('Date', axis=1)

def prettify_df(raw: pd.DataFrame) -> pd.DataFrame:
    pretty = raw.reset_index(drop=True)
    pretty = drop_names(pretty)
    pretty = pretty.drop('Release_Date', axis=1)
    pretty = convert_delta(pretty)
    pretty = explode_showndate(pretty)
    return pretty.reset_index(drop=True)