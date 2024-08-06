import pandas as pd
import os
from app.metadata import clean, missing, append_meta
from tqdm import tqdm
from typing import Tuple


def export_whole_meta() -> None:
    full, miss = iterate_over_raws()
    full.to_csv("data/full/cineasta_full.csv")
    missing.to_csv("data/full/cineasta_missing.csv")


def iterate_over_raws() -> Tuple[pd.DataFrame, pd.DataFrame]:
    raw_dir = "data/raw/"
    full = pd.DataFrame()
    miss = pd.DataFrame()

    for csv in tqdm(os.listdir(raw_dir)):
        cleanDf = append_meta(pd.read_csv(f"{raw_dir}{csv}"))
        lost = missing(cleanDf)

        cleanDf = clean(cleanDf)

        full = pd.concat([full, cleanDf], ignore_index=True)
        miss = pd.concat([miss, lost], ignore_index=True)

    return full, miss


def get_total_loss() -> float:
    raw_dir = "data/raw/"

    after = len(pd.read_csv("data/full/cineasta_full.csv"))
    before = sum(len(pd.read_csv(f"{raw_dir}{csv_file}")) for csv_file in os.listdir(raw_dir))

    return 100 - (after / before) * 100
