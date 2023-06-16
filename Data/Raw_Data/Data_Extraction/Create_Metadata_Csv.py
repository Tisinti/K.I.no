import time

from MovieSearch import MovieSearch
import timeit
import pandas as pd
from datetime import datetime


def str_to_date(string):
    return datetime.strptime(string, '%d.%m.%y').date()


if __name__ == "__main__":
    #print(time.process_time())
    #read raw data csv
    df = pd.read_csv("~/Projekte/Movie_Attendence_Prediction/Data/Raw_Data/CineAsta_Movie_Data_Raw.csv")
    # Convert the dates into right type
    df['Date'] = df['Date'].apply(str_to_date)
    #df['TMDB_TITLE'] = df['Movie'].astype(MovieSearch)
