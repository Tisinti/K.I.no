from flask import Flask, render_template, request
from dotenv import load_dotenv
from app.training import predict_attendance
from app.training import get_model, get_encoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder
import os
from sklearn.preprocessing import MaxAbsScaler

lin = LinearRegression()
ranfor = RandomForestRegressor()
ordenc = OrdinalEncoder()
max = MaxAbsScaler()

load_dotenv()

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def show():
    data = {'key': os.getenv('TMDB_API_KEY')}
    return render_template("index.html", data=data)

@app.route('/result', methods=['POST'])
def result():
    title = request.form['title']
    date = request.form['date']
    model, enc, scaler= get_model(ranfor), get_encoder(ordenc), get_encoder(max)

    res = predict_attendance(model=model, enc=enc, 
                             search=title, date=date, scaler=scaler)
    data = {'res': res, 'quip': quip(res)}
    return render_template('result.html', data=data)

def quip(res: int) -> str:
    if isinstance(res, str):
        return "Der Film hat scheinbar keine Bewertungen oder existiert nicht auf Letterboxd"
    if res < 3:
        return "Immer noch mehr als gestern 😓"
    if res >= 3 and res <= 10:
        return "Meist geschauter Arthouse Film"
    if res > 10 and res <= 30:
        return "🥳"
    if res > 30 and res < 50:
        return "Ryan Gosling detected (literally me)"
    else:
        return "HOLY FUCKING SHIT"
