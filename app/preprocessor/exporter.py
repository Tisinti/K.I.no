import glob
import os
import pandas as pd
from .cleaner import extract_wanted


def run_over_unformated(folder, extension):
    for file in glob.glob(f"{folder}*{extension}"):
        export_to_csv(file)


def export_to_csv(file):
    try:
        # normalize file name
        file_name = os.path.basename(file)
        file_name: str = os.path.splitext(file_name)[0]
        
        # last part of file name is the year
        year = file_name.split(" ")[-1]
        year = year.replace("-", "")

        # standardize file names
        file_name = file_name.lower()
        file_name = file_name.replace(" ", "_")
        if "wise" in file_name:
            file_name = f"winter_{year}"
        if "sose" in file_name:
            file_name = f"sommer_{year}"

        # read file into dataframe
        df = pd.read_excel(file)
        if "Unnamed" in df.columns[0]:
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        # cut and format dataframe appropriatly
        content = extract_wanted(df, year)

        # Don't write the csv if the dataframe is empty
        if content.empty:
            return

        # export dataframe as .csv file
        content.to_csv(f"data/raw/{file_name}.csv", encoding="utf-8", index=False)

    except Exception as e:
        print(f"{file_name} did not go through. Error {e}")


def execute_export():
    folder = "data/unformatted/"
    extension = [".xls", ".xlsx", ".ods"]

    for ext in extension:
        run_over_unformated(folder, ext)
