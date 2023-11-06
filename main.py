from app.collector import export_whole_meta, get_total_loss
from app.metadata import clean, missing, append_meta
from app.analysis import createAllPlotsPipe
from app.utils import SearchMovie
import pandas as pd 

raw_dir = 'data/raw/winter_0506.csv'

def get_clean_meta():
    return clean(append_meta(pd.read_csv(raw_dir)))

if __name__ == "__main__":
    print(len(pd.read_csv("data/full/cineasta_missing.csv")))