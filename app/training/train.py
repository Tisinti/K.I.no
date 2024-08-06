from typing import Tuple

import pandas as pd
from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, MaxAbsScaler

from app.training import preprocess


def split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train, test = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)
    return train, test


def x_y_split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    return df.drop('Attendance', axis=1), df['Attendance']


def save_model(model) -> None:
    dump(model, f'models/model/{type(model).__name__}.joblib')


def save_encoder(enc) -> None:
    dump(enc, f'models/encoder/{type(enc).__name__}.joblib')


def run_training(df: pd.DataFrame, model) -> None:
    enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    scaler = MaxAbsScaler().set_output(transform="pandas")

    train = split(df)[0]
    train = preprocess(train, fit=True, enc=enc, scaler=scaler)
    X_train, y_train = x_y_split(train)

    fitted_model = model.fit(X_train, y_train)

    save_model(fitted_model)
    save_encoder(enc)
    save_encoder(scaler)


def get_model(model) -> object:
    return load(f'models/model/{type(model).__name__}.joblib')


def get_encoder(enc) -> object:
    return load(f'models/encoder/{type(enc).__name__}.joblib')
