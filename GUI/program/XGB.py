from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import catboost as ctb
import pandas as pd
import requests
import datetime as dt
import time
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV

df2 = pd.read_csv('BTC-KRW2.csv')
df = df2.drop(['RSI', 'Change_rate'], axis=1)
df

df = df.set_index("Date")
df.reset_index(drop=False, inplace=True)

lag_features = ["Open", "High", "Low", "Volume"]

window1 = 3
window2 = 7
window3 = 30

df_rolled_3d = df[lag_features].rolling(window=window1, min_periods=0)
df_rolled_7d = df[lag_features].rolling(window=window2, min_periods=0)
df_rolled_30d = df[lag_features].rolling(window=window3, min_periods=0)

df_mean_3d = df_rolled_3d.mean().shift(1).reset_index()
df_mean_7d = df_rolled_7d.mean().shift(1).reset_index()
df_mean_30d = df_rolled_30d.mean().shift(1).reset_index()

df_std_3d = df_rolled_3d.std().shift(1).reset_index()
df_std_7d = df_rolled_7d.std().shift(1).reset_index()
df_std_30d = df_rolled_30d.std().shift(1).reset_index()

for feature in lag_features:
    df[f"{feature}_mean_lag{window1}"] = df_mean_3d[feature]
    df[f"{feature}_mean_lag{window2}"] = df_mean_7d[feature]
    df[f"{feature}_mean_lag{window3}"] = df_mean_30d[feature]

    df[f"{feature}_std_lag{window1}"] = df_std_3d[feature]
    df[f"{feature}_std_lag{window2}"] = df_std_7d[feature]
    df[f"{feature}_std_lag{window3}"] = df_std_30d[feature]

df.fillna(df.mean(), inplace=True)

df.set_index("Date", drop=False, inplace=True)
df.head()

df = df[df['Date'] >= '2021-01-01 00:00:00']
df_train = df[:17220]
df_valid = df[17220:]

print('train shape :', df_train.shape)
print('validation shape :', df_valid.shape)

import pmdarima as pm
exogenous_features = ["Open", "High", "Low","Volume"]

X_train, y_train = df_train[exogenous_features], df_train.Close
X_test, y_test = df_valid[exogenous_features], df_valid.Close

reg = xgb.XGBRegressor()

params = {
    "learning_rate": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
    "max_depth": [1, 3, 4, 5, 6, 7],
    "n_estimators": [int(x) for x in np.linspace(start=100, stop=2000, num=10)],
    "min_child_weight": [int(x) for x in np.arange(3, 15, 1)],
    "gamma": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "subsample": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "colsample_bytree": [0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "colsample_bylevel": [0.5, 0.6, 0.7, 0.8, 0.9, 1],

}

model  = RandomizedSearchCV(
                reg,
                param_distributions=params,
                n_iter=10,
                n_jobs=-1,
                cv=5,
                verbose=3,
)
model.fit(X_train, y_train)

print(f"Model Best Score : {model.best_score_}")
print(f"Model Best Parameters : {model.best_estimator_.get_params()}")

model.best_estimator_

df_train['Predicted_Close_Price'] = model.predict(X_train)

df_train[['Close','Predicted_Close_Price']].plot(figsize=(15, 5))

df_valid['Forecast_XGBoost'] = model.predict(X_test)

overall_data = pd.concat([df_train, df_valid], sort=False)

from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score

train_mae = mean_absolute_error(df_train['Close'], df_train['Predicted_Close_Price'])
train_rmse = np.sqrt(mean_squared_error(df_train['Close'], df_train['Predicted_Close_Price']))
train_r2 = r2_score(df_train['Close'], df_train['Predicted_Close_Price'])

print(f"train MAE : {train_mae}")
print(f"train RMSE : {train_rmse}")
print(f"train R2 : {train_r2}")

test_mae = mean_absolute_error(df_valid['Close'], df_valid['Forecast_XGBoost'])
test_rmse = np.sqrt(mean_squared_error(df_valid['Close'], df_valid['Forecast_XGBoost']))
test_r2 = r2_score(df_valid['Close'], df_valid['Forecast_XGBoost'])

print(f"test MAE : {test_mae}")
print(f"test RMSE : {test_rmse}")
print(f"test R2 : {test_r2}")

import joblib
joblib.dump(model, './xgb_model2.pkl')