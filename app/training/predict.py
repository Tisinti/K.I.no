from datetime import datetime as dt
import pandas as pd
from app.metadata import append_meta
from app.training import preprocess

def predict_attendance(search, date, model, enc, scaler):
    date = dt.strptime(date, "%d.%m.%Y")
    query = pd.DataFrame(list(zip([search],[date], [None])))
    query.columns= ['Titel', 'Date', 'Attendance']
    
    res = append_meta(query)
    if res['Rating'].isnull().values.any():
        res['Rating'] = 5.0
    if res.loc[:, res.columns != 'Attendance'].isnull().values.any():
        return "DIE SUCHE WAR NICHT ERFOLGREICH \nKEINE PREDICTION MÖGLICH"

    res[['Release_Date', 'Date']] = res[['Release_Date', 'Date']].apply(pd.to_datetime)
    res = preprocess(res, fit=False, enc=enc, scaler=scaler)
    res = res.drop("Attendance", axis=1)

    return round(model.predict(res).mean())



    