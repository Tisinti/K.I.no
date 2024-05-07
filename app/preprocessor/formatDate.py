from datetime import datetime as dt
#convert dates that are Str into date type
#if the date is a String it is formated as "24.12." 
#year gets extracted from filename: 2 possible types XX or XXYY

def convert_date(year, date):
    #format example: "03.05.2007"
    format = "%d.%m.%y"

    try:
        #is date a string and year of type XX?
        if (isinstance(date, str)) and (len(year) == 2):
            date = date + year

        #is date a string and year of type XXYY?
        elif (isinstance(date, str)) and (len(year) > 2): 
            #XXYY (len = 4) implies that it's a wintersemester (starts 01.10, ends 01.04)
            #if month is bigger than 6 choose XX
            if int(date[3:-1]) > 6:
                date = date + year[:-2]
            #else choose YY as year
            else:
                date = date + year[2:]

        #if non of the above is true, date is already date type
        else:
            return date 
        
        #turn the formated date string into date type and return
        return dt.strptime(date, format)
    
    except Exception: 
        #catched exception means that final date string could not be converted to date type
        #which implies that we want to ignore this 
        return None