from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import OrdinalEncoder
from app.training import preprocess
from joblib import dump, load
import pandas as pd

def split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train, test = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)
    return train, test

def x_y_split(df: pd.DataFrame):
    return df.drop('Attendance', axis=1), df['Attendance']

def save_model(model):
    dump(model, f'models/model/{type(model).__name__}.joblib')

def save_encoder(enc):
    dump(enc, 'models/encoder/ord_enc.joblib')


def run_training(df: pd.DataFrame, model) -> None:
    enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

    train = split(df)[0]
    train = preprocess(train, fit=True, enc=enc)
    X_train, y_train = x_y_split(train)

    fitted_model = model.fit(X_train, y_train)

    save_model(fitted_model)
    save_encoder(enc)

def get_model(model):
    return load(f'models/model/{type(model).__name__}.joblib')

def get_encoder():
    return load('models/encoder/ord_enc.joblib')
