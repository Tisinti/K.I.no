from app.collector import export_whole_meta
from app.metadata import clean
import pandas as pd 

def create_full_csv():
    export_whole_meta()
    return

def create_clean_metacsv():
    raw = pd.read_csv('data/raw/sommer_18.csv')
    return clean(raw)

if __name__ == "__main__":
    print(pd.read_csv("data/full/cineasta_full.csv").head())