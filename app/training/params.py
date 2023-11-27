grad_param = {
    "loss":['squared_error', 'absolute_error', 'huber'],
    "learning_rate": [0.01, 0.05, 0.1, 0.15, 0.2],
    "min_samples_split": [0.1, 0.3, 0.5],
    "min_samples_leaf": [0.1, 0.3, 0.5],
    "max_depth":[3,5,8],
    "max_features":["log2","sqrt"],
    "subsample":[0.5, 0.8, 0.9, 1.0],
    "criterion": ['friedman_mse', 'squared_error'],
    "n_estimators":[10]
    }
rf_param = {
    "min_samples_leaf": [0.75, 1],
    "max_features":["log2","sqrt"],
    "criterion": ['friedman_mse', 'squared_error', 'absolute_error', 'poisson'],
    }

