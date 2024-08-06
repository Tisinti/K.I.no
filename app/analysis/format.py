from dotenv import load_dotenv
import pandas as pd
import os
from typing import Tuple

load_dotenv()


def format_full_csv() -> pd.DataFrame:
    save = pd.read_csv(os.getenv("FULL_CSV"), parse_dates=['Date'])
    missing = pd.read_csv(os.getenv("MISSING_CSV"), parse_dates=['Date'])

    cine_data = pd.concat([save, missing], axis=0, ignore_index=True)
    cine_data['MovieAge'] = pd.to_timedelta(cine_data['MovieAge'])
    cine_data = cine_data.drop(columns=["Unnamed: 0"])
    cine_data['year'] = cine_data['Semester'].str.split(" ").str[1]

    return cine_data


def cut_covid() -> Tuple[pd.DataFrame, pd.DataFrame]:
    cine_data = format_full_csv()
    # after covid
    after_covid = cine_data[cine_data['Date'] > pd.to_datetime('2020-03-01')]
    # before covid
    before_covid = cine_data[cine_data['Date'] < pd.to_datetime('2020-03-01')]

    return after_covid, before_covid


def get_save() -> Tuple[pd.DataFrame, pd.DataFrame]:
    save = pd.read_csv(os.getenv("FULL_CSV"), parse_dates=['Date'])

    after_save = save[save['Date'] > pd.to_datetime('2020-03-01')]
    # before covid
    before_save = save[save['Date'] < pd.to_datetime('2020-03-01')]

    return after_save, before_save


def add_bar_label(ax, index: pd.Index, curr_pos: int) -> int:
    for i, ind in enumerate(index):
        ax.annotate(str(ind), (curr_pos + i - 0.265, 2), rotation='vertical',
                    fontsize=7, color="w", style="oblique")
    return i + 1


def week_prepare(df: pd.DataFrame) -> pd.Series:
    grouped = df.groupby(['Weekday'])['Attendance'].mean()
    filtered = grouped[df.groupby(['Weekday'])['Attendance'].count() > 10]
    ordered = filtered.reindex(['Tuesday', 'Wednesday', 'Thursday'])

    return ordered
