from app.training import run_training, run_eval
from app.training import get_after_covid
from app.training import get_model, get_encoder
from app.training import predict_attendance
from app.training import run_cross_val
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor


after_covid = get_after_covid()
model = LinearRegression()

def train():
    run_training(after_covid, model)

def eval():
    linreg = get_model(model)
    enc = get_encoder()
    run_eval(after_covid, linreg, enc)

def prediction():
    eval()

    search = "Der Gott des Gemetzels"
    date = "22.11.2023"
    model = get_model(model)
    enc = get_encoder()
    
    print(predict_attendance(search, date, model, enc))

if __name__ == "__main__":
    train()
    eval()