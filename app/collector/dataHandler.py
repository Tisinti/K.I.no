import pandas as pd
import os  
from app.metadata import clean

def export_whole_meta():
    iterate_over_raws().to_csv("../data/full/cineasta_full.csv")
    return

def iterate_over_raws():
    raw_dir = "../data/raw/"
    full = pd.DataFrame()

    for csv in os.listdir(raw_dir):
        cleanDf = clean(pd.read_csv(csv))
        full = pd.concat([full, cleanDf], ignore_index=True)
    
    return full

