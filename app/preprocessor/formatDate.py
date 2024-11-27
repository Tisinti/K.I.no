from datetime import datetime as dt
from typing import Union


# Convert dates that are strings into date type
# If the date is a string, it is formatted as "24.12."
# Year gets extracted from filename: 2 possible types XX or XXYY

def convert_date(year: str, date: Union[str, dt]) -> Union[dt, None]:
    # Format example: "03.05.2007"
    date_format = "%d.%m.%y"

    try:
        # Is date a string and year of type XX?
        if isinstance(date, str) and len(year) == 2:
            date = date + year

        # Is date a string and year of type XXYY?
        elif isinstance(date, str) and len(year) > 2:
            # XXYY (len = 4) implies that it's a winter semester (starts 01.10, ends 01.04)
            # If month is greater than 6, choose XX
            if int(date[3:5]) > 6:
                date = date + year[:-2]
            # Else choose YY as year
            else:
                date = date + year[2:]

        # If none of the above is true, date is already date type
        else:
            return date

        # Turn the formatted date string into date type and return
        return dt.strptime(date, date_format)

    except Exception:
        # Caught exception means that final date string could not be converted to date type
        # Which implies that we want to ignore this
        return None
