import glob
import os
from typing import List

import pandas as pd

from .cleaner import extract_wanted


def run_over_unformatted(folder: str, extension: str) -> None:
    for file in glob.glob(f"{folder}*{extension}"):
        export_to_csv(file)


def export_to_csv(file: str) -> None:
    try:
        # Normalize file name
        file_name = os.path.basename(file)
        file_name, _ = os.path.splitext(file_name)

        # Last part of file name is the year
        year = file_name.split(" ")[-1]
        year = year.replace("-", "")

        # Standardize file names
        file_name = file_name.lower().replace(" ", "_")
        if "wise" in file_name:
            file_name = f"winter_{year}"
        elif "sose" in file_name:
            file_name = f"sommer_{year}"

        # Read file into DataFrame
        df = pd.read_excel(file)
        if "Unnamed" in df.columns[0]:
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        # Cut and format DataFrame appropriately
        content = extract_wanted(df, int(year))

        # Don't write the CSV if the DataFrame is empty
        if content.empty:
            return

        # Export DataFrame as .csv file
        content.to_csv(f"data/raw/{file_name}.csv", encoding="utf-8", index=False)

    except Exception as e:
        print(f"{file_name} did not go through. Error: {e}")


def execute_export() -> None:
    folder = "data/unformatted/"
    extensions: List[str] = [".xls", ".xlsx", ".ods"]

    for ext in extensions:
        run_over_unformatted(folder, ext)
