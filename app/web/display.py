import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder, MaxAbsScaler

from app.training import predict_attendance, get_model, get_encoder

load_dotenv()

lin = LinearRegression()
ranfor = RandomForestRegressor()
ordenc = OrdinalEncoder()
max_scaler = MaxAbsScaler()

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def show():
    data = {'key': os.getenv('TMDB_API_KEY')}
    return render_template("index.html", data=data)


@app.route('/result', methods=['POST'])
def result():
    title = request.form['title']
    date = request.form['date']
    model = get_model(ranfor)
    enc = get_encoder(ordenc)
    scaler = get_encoder(max_scaler)

    res = predict_attendance(search=title, date=date, model=model, enc=enc, scaler=scaler)
    data = {'res': res, 'quip': quip(res)}
    return render_template('result.html', data=data)


def quip(res: int) -> str:
    if isinstance(res, str):
        return "Der Film hat scheinbar keine Bewertungen oder existiert nicht auf Letterboxd"
    if res < 3:
        return "Immer noch mehr als gestern 😓"
    if 3 <= res <= 10:
        return "Meist geschauter Arthouse Film"
    if 10 < res <= 30:
        return "🥳"
    if 30 < res < 50:
        return "Ryan Gosling detected (literally me)"
    else:
        return "HOLY FUCKING SHIT"


if __name__ == "__main__":
    app.run()
