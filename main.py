from app.training import run_training, run_eval
from app.training import get_after_covid
from app.training import get_model, get_encoder
from app.training import predict_attendance
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

after_covid = get_after_covid()

rf = RandomForestRegressor(criterion='friedman_mse', max_features='sqrt')
lr = LinearRegression()
svr = SVR()

svr_param = {
    "kernel": ['poly', 'rbf', 'sigmoid'],
    "degree": [1, 2, 3],
    "gamma": ['scale'],
    "coef0": [-0.5, 0, 0.5],
    "C": [0.3, 0.5, 1]
    }
rf_param = {
    "min_samples_leaf": [0.75, 1],
    "max_features":["log2","sqrt"],
    "criterion": ['friedman_mse', 'squared_error', 'absolute_error', 'poisson'],
    }

clf = GridSearchCV(svr, param_grid=svr_param, cv = 5, n_jobs= -1,
                   scoring="neg_mean_absolute_error", verbose=2)

def train(model):
    run_training(after_covid, model)

def eval(model):
    sel_model = get_model(model)
    enc = get_encoder()
    run_eval(after_covid, sel_model, enc)
    return 

def predict(model):
    search = "I Origins"
    date = "28.11.2023"
    sel_model = get_model(model)
    enc = get_encoder()
    
    print(predict_attendance(search, date, sel_model, enc))

if __name__ == "__main__":
   #train(clf)
   predict(rf)