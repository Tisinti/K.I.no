import numpy as np
from pandas import DataFrame
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

from app.training import x_y_split, split, preprocess


def get_mse(model, X_test: np.ndarray, y_test: np.ndarray) -> float:
    predictions = model.predict(X_test)
    return mean_squared_error(y_test, predictions)


def get_mae(model, X_test: np.ndarray, y_test: np.ndarray) -> float:
    predictions = model.predict(X_test)
    return mean_absolute_error(y_test, predictions)


def run_cross_val(df: DataFrame, model, enc, scaler) -> float:
    """Run cross-validation and return the mean MAE."""
    n = 10
    scores = np.empty(n, dtype=float)

    for i in range(n):
        df = df.reset_index(drop=True)

        # Shuffle randomly for each fold
        train, test = train_test_split(df, test_size=0.2, shuffle=True)
        train = preprocess(train, fit=True, enc=enc, scaler=scaler)
        test = preprocess(test, fit=False, enc=enc, scaler=scaler)
        X_train, y_train = x_y_split(train)
        X_test, y_test = x_y_split(test)
        model.fit(X_train, y_train)
        scores[i] = get_mae(model, X_test, y_test)

    return scores.mean()


def run_eval(df: DataFrame, model, enc, scaler) -> None:
    test = split(df)[1]
    test = preprocess(test, fit=False, enc=enc, scaler=scaler)
    X_test, y_test = x_y_split(test)
    print(f"MAE: {get_mae(model, X_test, y_test)}")
    print(f"MSE: {get_mse(model, X_test, y_test)}")
    print(f"CROSS VALIDATION MAE: {run_cross_val(df, model, enc, scaler)}")
