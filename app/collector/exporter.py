import glob
import os
import pandas as pd
import re
from .cleaner import extract_wanted


def export_to_csv(folder, extension):
    for file in glob.glob(f"{folder}*{extension}"):
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
            
            #export dataframe as .csv file 
            content.to_csv(f"../data/raw_test/{file_name}.csv", encoding='utf-8', index = False)
        
        except:
            print(f"{file_name} did not go through.")

def execute_export():
    folder = "../../data/unformated/"
    extension = [".xls", ".xlsx", ".ods"]

    for ext in extension:
        export_to_csv(folder, ext)