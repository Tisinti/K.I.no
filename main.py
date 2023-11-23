from app.training import run_training, run_eval
from app.training import get_after_covid
from app.training import get_lin_reg, get_encoder
from app.training import predict_attendance
from app.training import run_cross_val

after_covid = get_after_covid()


def train_linreg():
    run_training(after_covid)

def eval_linreg():
    linreg = get_lin_reg()
    enc = get_encoder()
    run_eval(after_covid, linreg, enc)

def prediction():
    eval_linreg()

    search = "Der Gott des Gemetzels"
    date = "22.11.2023"
    model = get_lin_reg()
    enc = get_encoder()
    
    print(predict_attendance(search, date, model, enc))

if __name__ == "__main__":
    print(run_cross_val(after_covid))