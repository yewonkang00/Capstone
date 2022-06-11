import pandas as pd
import numpy as np
import math
import datetime as dt

import matplotlib.pyplot as plt
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns

from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler

from plotly.offline import plot, iplot, init_notebook_mode
init_notebook_mode(connected=True)

df2 = pd.read_csv('BTC-KRW2.csv')
data = df2.drop(['RSI', 'Change_rate'], axis=1)

closedf = data[['Date','Close','Open','High','Low','Volume']]
print("Shape of close dataframe:", closedf.shape[0])

closedf = closedf[closedf['Date'] >= '2021-01-01 00:00:00']
close_stock = closedf.copy()
print("Total data for prediction: ",closedf.shape[0])

del closedf['Date']
scaler=MinMaxScaler(feature_range=(0,1))
opendf = closedf['Open']
highdf = closedf['High']
lowdf = closedf['Low']
volumedf = closedf['Volume']
close = closedf['Close']

scaler=MinMaxScaler(feature_range=(0,1))
opendf = scaler.fit_transform(np.array(opendf).reshape(-1,1))
highdf = scaler.fit_transform(np.array(highdf).reshape(-1,1))
lowdf = scaler.fit_transform(np.array(lowdf).reshape(-1,1))
volumedf = scaler.fit_transform(np.array(volumedf).reshape(-1,1))
close = scaler.fit_transform(np.array(close).reshape(-1,1))

open_train_data = opendf[:17220]
open_test_data = opendf[17220:]

high_train_data = highdf[:17220]
high_test_data = highdf[17220:]

low_train_data = lowdf[:17220]
low_test_data = lowdf[17220:]

volume_train_data = volumedf[:17220]
volume_test_data = volumedf[17220:]

close_train_data = close[:17220]
close_test_data = close[17220:]

def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

time_step = 21
X_train_open, y_train_open = create_dataset(open_train_data, time_step)
X_test_open, y_test_open = create_dataset(open_test_data, time_step)

X_train_high, y_train_high = create_dataset(high_train_data, time_step)
X_test_high, y_test_high = create_dataset(high_test_data, time_step)

X_train_low, y_train_low = create_dataset(low_train_data, time_step)
X_test_low, y_test_low = create_dataset(low_test_data, time_step)

X_train_volume, y_train_volume = create_dataset(volume_train_data, time_step)
X_test_volume, y_test_volume = create_dataset(volume_test_data, time_step)

X_train_close, y_train_close = create_dataset(close_train_data, time_step)
X_test_close, y_test_close = create_dataset(close_test_data, time_step)

my_model_open = XGBRegressor(n_estimators=1000)
my_model_open.fit(X_train_open, y_train_open, verbose=False)

my_model_high = XGBRegressor(n_estimators=1000)
my_model_high.fit(X_train_high, y_train_high, verbose=False)

my_model_low = XGBRegressor(n_estimators=1000)
my_model_low.fit(X_train_low, y_train_low, verbose=False)

my_model_volume = XGBRegressor(n_estimators=1000)
my_model_volume.fit(X_train_volume, y_train_volume, verbose=False)

my_model_close = XGBRegressor(n_estimators=1000)
my_model_close.fit(X_train_close, y_train_close, verbose=False)

open_train_predict=my_model_open.predict(X_train_open)
open_test_predict=my_model_open.predict(X_test_open)

high_train_predict=my_model_high.predict(X_train_high)
high_test_predict=my_model_high.predict(X_test_high)

low_train_predict=my_model_low.predict(X_train_low)
low_test_predict=my_model_low.predict(X_test_low)

volume_train_predict=my_model_volume.predict(X_train_volume)
volume_test_predict=my_model_volume.predict(X_test_volume)

close_train_predict=my_model_close.predict(X_train_close)
close_test_predict=my_model_close.predict(X_test_close)

open_train_predict = open_train_predict.reshape(-1,1)
open_test_predict = open_test_predict.reshape(-1,1)

high_train_predict = high_train_predict.reshape(-1,1)
high_test_predict = high_test_predict.reshape(-1,1)

low_train_predict = low_train_predict.reshape(-1,1)
low_test_predict = low_test_predict.reshape(-1,1)

volume_train_predict = volume_train_predict.reshape(-1,1)
volume_test_predict = volume_test_predict.reshape(-1,1)

close_train_predict = close_train_predict.reshape(-1,1)
close_test_predict = close_test_predict.reshape(-1,1)

# Transform back to original form

open_train_predict = scaler.inverse_transform(open_train_predict)
open_test_predict = scaler.inverse_transform(open_test_predict)

high_train_predict = scaler.inverse_transform(high_train_predict)
high_test_predict = scaler.inverse_transform(high_test_predict)

low_train_predict = scaler.inverse_transform(low_train_predict)
low_test_predict = scaler.inverse_transform(low_test_predict)

volume_train_predict = scaler.inverse_transform(volume_train_predict)
volume_test_predict = scaler.inverse_transform(volume_test_predict)

close_train_predict = scaler.inverse_transform(close_train_predict)
close_test_predict = scaler.inverse_transform(close_test_predict)

open_original_ytrain = scaler.inverse_transform(y_train_open.reshape(-1,1))
open_original_ytest = scaler.inverse_transform(y_test_open.reshape(-1,1))

high_original_ytrain = scaler.inverse_transform(y_train_high.reshape(-1,1))
high_original_ytest = scaler.inverse_transform(y_test_high.reshape(-1,1))

low_ytrain = scaler.inverse_transform(y_train_low.reshape(-1,1))
low_ytest = scaler.inverse_transform(y_test_low.reshape(-1,1))

volume_ytrain = scaler.inverse_transform(y_train_volume.reshape(-1,1))
volume_ytest = scaler.inverse_transform(y_test_volume.reshape(-1,1))

close_ytrain = scaler.inverse_transform(y_train_close.reshape(-1,1))
close_ytest = scaler.inverse_transform(y_test_close.reshape(-1,1))

x_input = open_test_data[len(open_test_data) - time_step:].reshape(1, -1)
temp_input = list(x_input)
temp_input = temp_input[0].tolist()

from numpy import array

lst_output = []
n_steps = time_step
i = 0
pred_days = 10
while (i < pred_days):

    if (len(temp_input) > time_step):

        x_input = np.array(temp_input[1:])
        # print("{} day input {}".format(i,x_input))
        x_input = x_input.reshape(1, -1)

        yhat = my_model_open.predict(x_input)
        # print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat.tolist())
        temp_input = temp_input[1:]

        lst_output.extend(yhat.tolist())
        i = i + 1

    else:
        yhat = my_model_open.predict(x_input)

        temp_input.extend(yhat.tolist())
        lst_output.extend(yhat.tolist())

        i = i + 1

print("Output of predicted next days: ", len(lst_output))

last_days=np.arange(1,time_step+1)
day_pred=np.arange(time_step+1,time_step+pred_days+1)
print(last_days)
print(day_pred)

temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
temp_mat[:] = np.nan
temp_mat = temp_mat.reshape(1, -1).tolist()[0]

last_original_days_value = temp_mat
next_predicted_days_value = temp_mat

last_original_days_value[0:time_step + 1] = \
scaler.inverse_transform(opendf[len(opendf) - time_step:]).reshape(1, -1).tolist()[0]
next_predicted_days_value[time_step:] = \
scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

new_pred_plot = pd.DataFrame({
    'last_original_days_value': last_original_days_value,
    'next_predicted_days_value': next_predicted_days_value
})
next_predicted_days_value
xgb_test_data = pd.DataFrame(next_predicted_days_value)
xgb_test_data.columns = ['Open']
xgb_test_data

x_input = high_test_data[len(high_test_data) - time_step:].reshape(1, -1)
temp_input = list(x_input)
temp_input = temp_input[0].tolist()

from numpy import array

lst_output = []
n_steps = time_step
i = 0
pred_days = 10
while (i < pred_days):

    if (len(temp_input) > time_step):

        x_input = np.array(temp_input[1:])
        # print("{} day input {}".format(i,x_input))
        x_input = x_input.reshape(1, -1)

        yhat = my_model_high.predict(x_input)
        # print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat.tolist())
        temp_input = temp_input[1:]

        lst_output.extend(yhat.tolist())
        i = i + 1

    else:
        yhat = my_model_high.predict(x_input)

        temp_input.extend(yhat.tolist())
        lst_output.extend(yhat.tolist())

        i = i + 1

print("Output of predicted next days: ", len(lst_output))

temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
temp_mat[:] = np.nan
temp_mat = temp_mat.reshape(1, -1).tolist()[0]

last_original_days_value = temp_mat
next_predicted_days_value = temp_mat

last_original_days_value[0:time_step + 1] = \
scaler.inverse_transform(highdf[len(highdf) - time_step:]).reshape(1, -1).tolist()[0]
next_predicted_days_value[time_step:] = \
scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

new_pred_plot = pd.DataFrame({
    'last_original_days_value': last_original_days_value,
    'next_predicted_days_value': next_predicted_days_value
})

xgb_test_data['High'] = next_predicted_days_value
xgb_test_data

x_input = low_test_data[len(low_test_data) - time_step:].reshape(1, -1)
temp_input = list(x_input)
temp_input = temp_input[0].tolist()

from numpy import array

lst_output = []
n_steps = time_step
i = 0
pred_days = 10
while (i < pred_days):

    if (len(temp_input) > time_step):

        x_input = np.array(temp_input[1:])
        # print("{} day input {}".format(i,x_input))
        x_input = x_input.reshape(1, -1)

        yhat = my_model_low.predict(x_input)
        # print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat.tolist())
        temp_input = temp_input[1:]

        lst_output.extend(yhat.tolist())
        i = i + 1

    else:
        yhat = my_model_low.predict(x_input)

        temp_input.extend(yhat.tolist())
        lst_output.extend(yhat.tolist())

        i = i + 1

print("Output of predicted next days: ", len(lst_output))

temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
temp_mat[:] = np.nan
temp_mat = temp_mat.reshape(1, -1).tolist()[0]

last_original_days_value = temp_mat
next_predicted_days_value = temp_mat

last_original_days_value[0:time_step + 1] = \
scaler.inverse_transform(lowdf[len(lowdf) - time_step:]).reshape(1, -1).tolist()[0]
next_predicted_days_value[time_step:] = \
scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

new_pred_plot = pd.DataFrame({
    'last_original_days_value': last_original_days_value,
    'next_predicted_days_value': next_predicted_days_value
})

xgb_test_data['Low'] = next_predicted_days_value
xgb_test_data

x_input = volume_test_data[len(volume_test_data) - time_step:].reshape(1, -1)
temp_input = list(x_input)
temp_input = temp_input[0].tolist()

from numpy import array

lst_output = []
n_steps = time_step
i = 0
pred_days = 10
while (i < pred_days):

    if (len(temp_input) > time_step):

        x_input = np.array(temp_input[1:])
        # print("{} day input {}".format(i,x_input))
        x_input = x_input.reshape(1, -1)

        yhat = my_model_volume.predict(x_input)
        # print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat.tolist())
        temp_input = temp_input[1:]

        lst_output.extend(yhat.tolist())
        i = i + 1

    else:
        yhat = my_model_volume.predict(x_input)

        temp_input.extend(yhat.tolist())
        lst_output.extend(yhat.tolist())

        i = i + 1

print("Output of predicted next days: ", len(lst_output))

temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
temp_mat[:] = np.nan
temp_mat = temp_mat.reshape(1, -1).tolist()[0]

last_original_days_value = temp_mat
next_predicted_days_value = temp_mat

last_original_days_value[0:time_step + 1] = \
scaler.inverse_transform(volumedf[len(volumedf) - time_step:]).reshape(1, -1).tolist()[0]
next_predicted_days_value[time_step:] = \
scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

new_pred_plot = pd.DataFrame({
    'last_original_days_value': last_original_days_value,
    'next_predicted_days_value': next_predicted_days_value
})

xgb_test_data['Volume'] = next_predicted_days_value
xgb_test_data.to_csv('xgb_test_data.csv',index=False)

import joblib

loaded_model = joblib.load('./xgb_model2.pkl')
result = loaded_model.predict(xgb_test_data)
resultdf = pd.DataFrame(result)
resultdf.columns = ['predict']
resultdf['Date'] = pd.date_range("2022-06-09", "2022-07-09" ,freq="D")
resultdf

#fig = px.line(my_model,labels={'value': 'Open price','index': 'Timestamp'})
# fig = px.line(new_pred_plot,x=new_pred_plot.index, y=[new_pred_plot['last_original_days_value'],
#                                                       new_pred_plot['next_predicted_days_value']],
#               labels={'value': 'Open price','index': 'Date'})

plt = px.line(new_pred_plot,x=resultdf.Date, y=[resultdf['predict']],
              labels={'value': 'predict','index': 'Date'})
plt.update_layout(title_text='Predict next 10 days',
                  plot_bgcolor='white', font_size=15, font_color='black',legend_title_text='Close Price')
# fig.for_each_trace(lambda t:  t.update(name = next(names)))
plt.update_xaxes(showgrid=False)
plt.update_yaxes(showgrid=False)
# plt.imshow(img.reshape((28, 28)))
plt.show()