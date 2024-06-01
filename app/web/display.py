from fastapi import FastAPI
from dotenv import load_dotenv
from app.training import predict_attendance
from app.training import get_model, get_encoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MaxAbsScaler

lin = LinearRegression()
ranfor = RandomForestRegressor()
ordenc = OrdinalEncoder()
max = MaxAbsScaler()

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "World"}


@app.get("/prediction/{movie}")
async def predict(movie: str, date: str) -> dict:
    model, enc, scaler = get_model(ranfor), get_encoder(ordenc), get_encoder(max)
    prediction = predict_attendance(
        model=model, enc=enc, search=movie, date=date, scaler=scaler
    )
    return {"prediction": prediction}
