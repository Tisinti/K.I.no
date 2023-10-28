from app.collector import export_whole_meta
from app.metadata import clean
import pandas as pd 

def create_clean_metacsv():
    raw = pd.read_csv('data/raw/sommer_18.csv')
    return clean(raw)

if __name__ == "__main__":
    export_whole_meta()