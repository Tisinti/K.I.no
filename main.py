from app.training import run_training, run_eval
from app.training import get_after_covid, get_full
from app.training import get_model, get_encoder
from app.training import predict_attendance
from sklearn.linear_model import Lasso, LinearRegression, Ridge, BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MaxAbsScaler

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


def train(model):
    run_training(after_covid, model)

def eval(model):
    sel_model = get_model(model)
    encoder = get_encoder(enc)
    max_scaler = get_encoder(scaler)
    run_eval(after_covid, sel_model, encoder, max_scaler)
    return 

def predict(model):
    search = "Barbie"
    date = "05.12.2023"
    sel_model = get_model(model)
    encoder = get_encoder(enc)
    max_scaler = get_encoder(scaler)

    print(f"\nPREDICTION FOR MOVIE: {search}")
    print(predict_attendance(search, date, sel_model, encoder, max_scaler), "\n")

if __name__ == "__main__":
   for model in [rf,lr,svr,lasso,ridge,gb,br]:
       print("----------------------------------------")
       print(f"CURRENT MODEL: {type(model).__name__} \n")
       print("EVALUATION:")
       eval(model)
       predict(model)
       
   