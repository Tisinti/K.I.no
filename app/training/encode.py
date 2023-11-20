import pandas as pd

def drop_names(full: pd.DataFrame) -> pd.DataFrame:
    full['Semester'] = full['Semester'].str.split(" ").str[0]
    return full.drop(['OG_Title', 'TMDB_Title'], axis = 1)

def explode_release(final: pd.DataFrame) -> pd.DataFrame:
    release = final['Release_Date']
    final['Release_Day'], final['Release_Month'], final['Release_Year'] = release.dt.day, release.dt.month, release.dt.year
    return final.drop('Release_Date', axis=1)

def explode_genre(final: pd.DataFrame) -> pd.DataFrame:
    if type(final['Genre'][0]) != list:
        final['Genre'] = final['Genre'].apply(lambda x: x[1:-1].replace(' ', '').replace("'", '').split(','))
    final = final.explode('Genre')
    return final

def convert_delta(final: pd.DataFrame) -> pd.DataFrame:
    final['MovieAge'] = pd.to_timedelta(final['MovieAge']).dt.days
    return final

def explode_showndate(final: pd.DataFrame) -> pd.DataFrame:
    shown = final['Date']
    final['ShownDate'], final['ShownMonth'] = shown.dt.day, shown.dt.month
    return final.drop('Date', axis=1)

def prettify_df(raw: pd.DataFrame) -> pd.DataFrame:
    pretty = raw.reset_index(drop=True)
    pretty = drop_names(pretty)
    pretty = explode_release(pretty)
    pretty = convert_delta(pretty)
    pretty = explode_showndate(pretty)
    return pretty.reset_index(drop=True)