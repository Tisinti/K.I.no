import glob
import os
import pandas as pd
import re
from .cleaner import extract_wanted


def run_over_unformated(folder, extension):
    for file in glob.glob(f"{folder}*{extension}"):
        export_to_csv(file)
    return

def export_to_csv(file):
    try:
        #normalize file name
        file_name = os.path.basename(file).lower()
        #remove extension and format for export
        file_name = os.path.splitext(file_name)[0]
        file_name = re.sub(" ", "_", file_name)

        #last part of file name is the year
        year = re.split("_", file_name)[1]
        
        #read file into dataframe
        df = pd.read_excel(file)
        
        #cut and format dataframe appropriatly 
        content = extract_wanted(df, year)
        
        # Don't write the csv if the datframe is empty
        if content.empty:
            return 

        #export dataframe as .csv file 
        content.to_csv(f"data/raw/{file_name}.csv", encoding='utf-8', index = False)
    
    except Exception as e:
        print(f"{file_name} did not go through. Error {e}")

def execute_export():
    folder = "data/unformated/"
    extension = [".xls", ".xlsx", ".ods"]

    for ext in extension:
        run_over_unformated(folder, ext)