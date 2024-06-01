from dotenv import load_dotenv
import pandas as pd
import os
load_dotenv()


def formatfullCSV():
    save = pd.read_csv(os.getenv("FULL_CSV"), parse_dates=['Date'])
    missing = pd.read_csv(os.getenv("MISSING_CSV"), parse_dates=['Date'])

    cineData = pd.concat([save, missing], axis=0, ignore_index=True)
    cineData['MovieAge'] = pd.to_timedelta(cineData['MovieAge'])
    cineData = cineData.drop(columns=["Unnamed: 0"])
    cineData['year'] = cineData['Semester'].str.split(" ").str[1]
    
    return cineData

def cutCovid():
    cineData = formatfullCSV()
    #after covid
    a_cov = cineData[cineData['Date'] > pd.to_datetime('2020-3-1')]
    #before covid
    b_cov = cineData[cineData['Date'] < pd.to_datetime('2020-3-1')]
    
    return a_cov, b_cov

def getSave():
    save = pd.read_csv(os.getenv("FULL_CSV"), parse_dates=['Date'])

    a_save = save[save['Date'] > pd.to_datetime('2020-3-1')]
    #before covid
    b_save = save[save['Date'] < pd.to_datetime('2020-3-1')]

    return a_save, b_save

def add_bar_label(ax, index, currPos):
    for i, ind in enumerate(index):
        ax.annotate(str(ind), (currPos+i - 0.265, 2), rotation = 'vertical', 
                    fontsize = 7, color = "w", style = "oblique")
    return i + 1

def week_prepare(df: pd.DataFrame) -> pd.Series:
    aha = df
    df = df.groupby(['Weekday'])['Attendance'].mean()
    df = df[aha.groupby(['Weekday'])['Attendance'].count() > 10]
    df = df.reindex(['Tuesday', 'Wednesday', "Thursday"])
    df = df.drop(columns=['count'])
    
    return df
