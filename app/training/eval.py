from sklearn.metrics import mean_squared_error, mean_absolute_error 
from app.training import target_prep, split, preprocess

def get_mse(model, X_test, y_test):
    predictions = model.predict(X_test) 
    return f'mean_squared_error :  {mean_squared_error(y_test, predictions)}'

def get_mae(model, X_test, y_test):
    predictions = model.predict(X_test) 
    return f'mean_absolute_error : {mean_absolute_error(y_test, predictions)}'

def run_eval(df, model, enc):
    test = split(df)[1]
    test = preprocess(test, fit=False, enc=enc)
    X_test, y_test = target_prep(test)
    print(get_mae(model, X_test, y_test))
    print(get_mse(model, X_test, y_test))
    
