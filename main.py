from app.training import run_training, run_eval
from app.training import get_after_covid
from app.training import get_model, get_encoder
from app.training import predict_attendance
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

after_covid = get_after_covid()

rf = RandomForestRegressor(criterion='friedman_mse', max_features='sqrt')
lr = LinearRegression()

def train(model):
    run_training(after_covid, model)

def eval(model):
    sel_model = get_model(model)
    enc = get_encoder()
    run_eval(after_covid, sel_model, enc)
    return 

def predict(model):
    search = "Mona Lisa and the Blood Moon"
    date = "05.12.2023"
    sel_model = get_model(model)
    enc = get_encoder()
    
    print(predict_attendance(search, date, sel_model, enc))

if __name__ == "__main__":
   eval(lr)
   eval(rf)
   predict(lr)
   predict(rf)