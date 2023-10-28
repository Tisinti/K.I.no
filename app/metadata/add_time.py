from datetime import datetime
import pandas as pd
import calendar


def add_semester(date: datetime):
    # Year is not important here as we only want to check Month!
    if date.month > datetime(2000, 3, 1).month and date.month < datetime(2000, 8, 1).month:
        return "Sommersemester"
    return "Wintersemester"

def date_to_weekday(date: datetime):
    return calendar.day_name[date.weekday()]

def movie_age(relaseDate: pd.Series, shownDate: pd.Series):
    return (pd.to_datetime(shownDate) - pd.to_datetime(relaseDate))