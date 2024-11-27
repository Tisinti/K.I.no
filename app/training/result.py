from sklearn.base import BaseEstimator
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge, BayesianRidge
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OrdinalEncoder, MaxAbsScaler
from sklearn.svm import SVR

from app.training import run_training, run_eval, get_after_covid, get_model, get_encoder, predict_attendance

after_covid = get_after_covid()
enc = OrdinalEncoder()
scaler = MaxAbsScaler()

rf = RandomForestRegressor(criterion='friedman_mse', max_features='sqrt')
lr = LinearRegression()
svr = SVR()
lasso = Lasso()
ridge = Ridge()
gb = GradientBoostingRegressor()
br = BayesianRidge()
knn = KNeighborsRegressor()

svr_param = {
    "kernel": ['poly', 'rbf', 'sigmoid'],
    "degree": [1, 2, 3],
    "gamma": ['scale'],
    "coef0": [-0.5, 0, 0.5],
    "C": [0.3, 0.5, 1]
}
rf_param = {
    "min_samples_leaf": [0.75, 1],
    "max_features": ["log2", "sqrt"],
    "criterion": ['friedman_mse', 'squared_error', 'absolute_error', 'poisson'],
}

clf = GridSearchCV(svr, param_grid=svr_param, cv=5, n_jobs=-1, scoring="neg_mean_absolute_error", verbose=2)


def train(model: BaseEstimator) -> None:
    run_training(after_covid, model)


def eval(model: BaseEstimator) -> None:
    sel_model = get_model(model)
    encoder = get_encoder(enc)
    max_scaler = get_encoder(scaler)
    run_eval(after_covid, sel_model, encoder, max_scaler)


def predict(model: BaseEstimator) -> None:
    search = "Skinamarink"
    date = "14.05.2024"
    sel_model = get_model(model)
    encoder = get_encoder(enc)
    max_scaler = get_encoder(scaler)

    print(f"\nPREDICTION FOR MOVIE: {search}")
    print(predict_attendance(search, date, sel_model, encoder, max_scaler), "\n")


def iterate_models() -> None:
    for model in [rf, lr, svr, lasso, ridge, gb, br, knn]:
        print("----------------------------------------")
        print(f"CURRENT MODEL: {type(model).__name__} \n")
        print("EVALUATION:")
        eval(model)
        predict(model)
