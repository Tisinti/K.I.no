from app.training import run_training, run_eval
from app.training import get_after_covid
from app.training import get_lin_reg, get_encoder
from app.training import predict_attendance


after_covid = get_after_covid()


def train_linreg():
    run_training(after_covid)

def eval_linreg():
    linreg = get_lin_reg()
    enc = get_encoder()
    run_eval(after_covid, linreg, enc)

if __name__ == "__main__":
    train_linreg()

    search = "Mona Lisa and the Blood Moon"
    date = "21.11.2023"
    model = get_lin_reg()
    enc = get_encoder()
    
    print(predict_attendance(search, date, model, enc))