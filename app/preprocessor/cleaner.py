import re

import pandas as pd

from .formatDate import convert_date


# Remove unwanted characters from the title
def clean_title(title: str) -> str:
    # List of words we want to delete
    naughty_list = ["OmU", "OmeU", "OV", "Klassiker:"]
    # Check titles and remove if something matches
    for scratch in naughty_list:
        title = re.sub(f"{scratch}", "", title)

    title = re.sub(r"\(.*\)", "", title)
    title = re.sub(r"\*", "", title)
    title = title.strip()
    return title


def extract_wanted(df: pd.DataFrame, year: int) -> pd.DataFrame:
    # Convert dates because there sometimes are no years appended like 28.10.
    df['Datum'] = df.apply(lambda x: convert_date(year, x['Datum']), axis=1)

    # Only use rows with dates
    df = df.dropna(subset=['Datum'])

    # Only keep date, name, attendance
    try:
        df = df[["Datum", "Titel", "Zuschauer"]]
    except KeyError:
        df = df[["Datum", "Titel", "Besucher"]]

    # New column names
    df.columns = ['Date', "Titel", "Attendance"]

    # Convert attendance type from float to int
    df = df.dropna(subset=["Attendance"])
    df['Attendance'] = df['Attendance'].astype(int)

    # Remove words that are not part of the title
    df['Titel'] = df['Titel'].apply(clean_title)
    return df
