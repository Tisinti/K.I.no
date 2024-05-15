import pandas as pd
import os
from app.metadata import clean, missing, append_meta
from tqdm import tqdm


def export_whole_meta():
    full, missing = iterate_over_raws()
    full.to_csv("data/full/cineasta_full.csv")
    missing.to_csv("data/full/cineasta_missing.csv")


def iterate_over_raws():
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


def get_total_loss():
    raw_dir = "data/raw/"

    after = len(pd.read_csv("data/full/cineasta_full.csv"))
    before = 0

    for csv in os.listdir(raw_dir):
        before += len(pd.read_csv(f"{raw_dir}{csv}"))

    return 100 - (after / before) * 100
