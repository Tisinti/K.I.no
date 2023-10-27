from app.metadata import clean
from app.collector import export_whole_meta
import pandas as pd 

def create_clean_metacsv():
    raw = pd.read_csv('data/raw/winter_2223.csv')
    return clean(raw)

if __name__ == "__main__":
    export_whole_meta()
