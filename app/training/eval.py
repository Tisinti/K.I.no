from sklearn.metrics import mean_squared_error, mean_absolute_error
from app.training import x_y_split, split, preprocess
from sklearn.model_selection import train_test_split
from pandas import DataFrame
import numpy as np


def get_mse(model, X_test, y_test):
    predictions = model.predict(X_test)
    return mean_squared_error(y_test, predictions)


def get_mae(model, X_test, y_test):
    predictions = model.predict(X_test)
    return mean_absolute_error(y_test, predictions)


def run_cross_val(df: DataFrame, model, enc, scaler) -> np.array:
    """I HATE THIS"""
    n = 10
    score = np.empty(n, dtype=float)

    for i in range(0, n):
        df = df.reset_index(drop=True)

        # Shuffle randomly for each fold
        train, test = train_test_split(df, test_size=0.2, shuffle=True)
        train, test = (
            preprocess(train, fit=True, enc=enc, scaler=scaler),
            preprocess(test, fit=False, enc=enc, scaler=scaler),
        )
        X_train, y_train = x_y_split(train)
        X_test, y_test = x_y_split(test)
        model.fit(X_train, y_train)
        score[i] = get_mae(model, X_test, y_test)

    return score.mean()


def run_eval(df, model, enc, scaler):
    test = split(df)[1]
    test = preprocess(test, fit=False, enc=enc, scaler=scaler)
    X_test, y_test = x_y_split(test)
    print(f"MAE: {get_mae(model, X_test, y_test)}")
    print(f"MSE: {get_mse(model, X_test, y_test)}")
    print(f"CROSS VALIDATION MAE: {run_cross_val(df, model, enc, scaler)}")
