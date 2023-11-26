from sklearn.metrics import mean_squared_error, mean_absolute_error 
from app.training import x_y_split, split, preprocess
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LinearRegression
from pandas import DataFrame
import numpy as np

def get_mse(model, X_test, y_test):
    predictions = model.predict(X_test) 
    return mean_squared_error(y_test, predictions)

def get_mae(model, X_test, y_test):
    predictions = model.predict(X_test) 
    return mean_absolute_error(y_test, predictions)

def run_cross_val(df: DataFrame) -> list[float]:
    """ I HATE THIS """
    n = 5
    skf = StratifiedKFold(n_splits=n, shuffle=True, random_state=42)
    model = LinearRegression()
    X, y = x_y_split(df)
    score = np.empty(n, dtype=float)
    
    for i, (train_index, test_index) in enumerate(skf.split(X, y)):
        df = df.reset_index(drop=True)
        enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

        train = df.filter(items=list(train_index), axis=0)
        test = df.filter(items=list(test_index), axis=0)
        train, test = preprocess(train, fit=True, enc=enc), preprocess(test, fit=False, enc=enc)
        X_train, y_train = x_y_split(train)
        X_test, y_test = x_y_split(test)
        model.fit(X_train, y_train)
        score[i] = get_mae(model, X_test, y_test)
    
    return score.mean()

def run_eval(df, model, enc):
    test = split(df)[1]
    test = preprocess(test, fit=False, enc=enc)
    X_test, y_test = x_y_split(test)
    print(get_mae(model, X_test, y_test))
    print(get_mse(model, X_test, y_test))
    
