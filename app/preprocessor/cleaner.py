import re
from .formatDate import convert_date

#remove unwanted characters from the title
def clean_title(title):
    #list of words we want to delete
    naughty_list = [' \(OmU\)', " \(OV\)", " OmU", " OmeU", " OV"]
    #check titles and remove if something matches
    for scratch in naughty_list:
        title = re.sub(scratch, "", title)
    return title

def extract_wanted(df, year):
    #convert_dates because there sometimes are no years appended like 28.10.
    df['Datum'] = df.apply(lambda x: convert_date(year, x['Datum']), axis=1)

    #only use rows with dates
    df = df.dropna(subset= 'Datum')
    
    #only keep date, name, attendance
    try:
        df = df[["Datum", "Titel", "Zuschauer"]]
    except Exception:
        df = df[["Datum", "Titel", "Besucher"]]
    
    #New Column Names
    df.columns = ['Date', "Titel", "Attendance"]
    
    #Convert Attendance Type from float to int
    df = df.dropna(subset= "Attendance")
    df['Attendance'] = df['Attendance'].astype(int)
    
    #remove words that are not part of the title
    df['Titel'] = df['Titel'].apply(clean_title)
    return df