import warnings

warnings.filterwarnings('ignore')

import warnings

import numpy as np
import pandas as pd # type: ignore
import polars as pl

warnings.filterwarnings('ignore')
pd.options.display.max_columns = None

class CONFIG:
    seed = 42
    target_col = "responder_6"
    feature_cols = ["symbol_id", "time_id"] \
        + [f"feature_{idx:02d}" for idx in range(79)] \
        + [f"responder_{idx}_lag_1" for idx in range(9)]
    
train = pl.scan_parquet("/kaggle/input/js24-preprocessing-create-lags/training.parquet").collect().to_pandas()
valid = pl.scan_parquet("/kaggle/input/js24-preprocessing-create-lags/validation.parquet").collect().to_pandas()

import warnings

warnings.filterwarnings('ignore')

import os

import numpy as np
import pandas as pd
import polars as pl
import xgboost as xgb
from ray import tune
from ray.tune.schedulers import ASHAScheduler
from sklearn.metrics import r2_score # type: ignore

# Prepare training and validation data
X_train = train[CONFIG.feature_cols]
y_train = train[CONFIG.target_col]
w_train = train["weight"]

X_valid = valid[CONFIG.feature_cols]
y_valid = valid[CONFIG.target_col]
w_valid = valid["weight"]

def train_xgb(config):
    # Merge default parameters with the tuning parameters
    params = {
        'objective': 'reg:squarederror',
        'eval_metric': 'rmse',
        'tree_method': 'gpu_hist',
        'random_state': CONFIG.seed,
        **config  # Hyperparameters from Ray Tune
    }

    # Create DMatrix objects
    Xy_train = xgb.DMatrix(X_train, label=y_train, weight=w_train)
    Xy_valid = xgb.DMatrix(X_valid, label=y_valid, weight=w_valid)

    evals = [(Xy_train, 'train'), (Xy_valid, 'valid')]

    # Train the model
    model = xgb.train(
        params=params,
        dtrain=Xy_train,
        num_boost_round=2000,
        evals=evals,
        early_stopping_rounds=50,
        verbose_eval=False
    )

    # Predict on validation set
    y_pred_valid = model.predict(Xy_valid)

    # Calculate R2 score
    valid_score = r2_score(y_valid, y_pred_valid, sample_weight=w_valid)

    # Send the score to Ray Tune
    tune.report(valid_score=valid_score)

# Define the hyperparameter search space
search_space = {
    'learning_rate': tune.loguniform(1e-4, 1e-1),
    'max_depth': tune.randint(3, 10),
    'subsample': tune.uniform(0.5, 1.0),
    'colsample_bytree': tune.uniform(0.5, 1.0),
    'reg_alpha': tune.loguniform(1e-2, 10.0),
    'reg_lambda': tune.loguniform(1e-2, 10.0),
}

# Set up the scheduler for early stopping
scheduler = ASHAScheduler(
    metric='valid_score',
    mode='max',
    max_t=2000,
    grace_period=10,
    reduction_factor=2
)

# Run hyperparameter tuning with Ray Tune
analysis = tune.run(
    train_xgb,
    resources_per_trial={'cpu': 1, 'gpu': 1},
    config=search_space,
    num_samples=50,
    scheduler=scheduler
)

# Output the best hyperparameters
print("Best hyperparameters found:")
print(analysis.best_config)