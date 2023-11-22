from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import OrdinalEncoder
from app.training import preprocess
from joblib import dump, load
import pandas as pd

def split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train, test = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)
    return train, test

def feature_prep(train: pd.DataFrame):
    return train.drop('Attendance', axis=1), train['Attendance']

def target_prep(test: pd.DataFrame):
    return test.drop('Attendance', axis=1), test['Attendance']

def training(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train) 
    return model

def save_model(model):
    dump(model, 'models/model/lin_reg_proto.joblib')

def save_encoder(enc):
    dump(enc, 'models/encoder/lin_reg_enc.joblib')


def run_training(df: pd.DataFrame) -> None:
    enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

    train = split(df)[0]
    train = preprocess(train, fit=True, enc=enc)
    X_train, y_train = feature_prep(train)
    lin_reg = training(X_train, y_train)
    save_model(lin_reg)
    save_encoder(enc)

def get_lin_reg():
    return load('models/model/lin_reg_proto.joblib')

def get_encoder():
    return load('models/encoder/lin_reg_enc.joblib')
